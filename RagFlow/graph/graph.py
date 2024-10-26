from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from  RagFlow.graph.consts import RETRIEVE,  GRADE_DOCUMENTS, GENERATE, WEBSEARCH
from RagFlow.graph.nodes import generate, grade_documents, StateRetrieve, tavily_web_search
from RagFlow.graph.state import GraphState
from RagFlow.graph.chains.hallucination_grader import  hallucination_grader
from RagFlow.graph.chains.answer_grader import  answer_grader
from RagFlow.graph.chains.router import question_router

load_dotenv()


def decide_to_generate(state):
    print("++++++++++Asses Node Graph+++++++++")

    if state["web_search"]:
        print("------Not Relevant Document------")
        return  WEBSEARCH
    else:

        print("------Relevant Document------")
        return GENERATE
def decide_generaton_grounded_in_documents_and_questions(state: GraphState):
    print("=====check Hallucination=====")
    question=state["question"]
    generation= state["generation"]
    document= state["documents"]
    score= hallucination_grader.invoke({
        "documents":document, "generation":generation
    })
    if score.binary_score:
        print("====Not Halllucinated=======")
        score=answer_grader.invoke({
            "question":question,
            "generation":generation
        })
        if score.binary_score:
            return "useful"
        else:
            return "not useful"
    else:
        return "not supported"
def route_question(state:GraphState):
    print("====Route Question=====")
    question= state["question"]
    source=question_router.invoke({"question":question})
    if source.datasource==WEBSEARCH:
        return WEBSEARCH
    else:
        return RETRIEVE

stateretrieve=StateRetrieve()
workflow=StateGraph(GraphState)
workflow.add_node(RETRIEVE, stateretrieve.retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, tavily_web_search)

# workflow.set_entry_point(RETRIEVE)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.set_conditional_entry_point(
    route_question,
    {
        WEBSEARCH:WEBSEARCH,
        RETRIEVE:RETRIEVE
    }
)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    {
        WEBSEARCH:WEBSEARCH,
     GENERATE:GENERATE,
     },

)
workflow.add_conditional_edges(
    GENERATE,
    decide_generaton_grounded_in_documents_and_questions,
    {
        "not supported": GENERATE,
        "useful": END,
        "not useful": WEBSEARCH
    }

)
workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(GENERATE, END)

app = workflow.compile()
app.get_graph().draw_mermaid_png(output_file_path="graph.png")