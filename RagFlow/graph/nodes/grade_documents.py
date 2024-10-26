from typing import List, Any,Dict

from langchain.chains.hyde.prompts import web_search
from sympy import gamma

from RagFlow.graph.state import GraphState
from RagFlow.graph.chains.retrieval_grader import  retrieval_grader

def grade_documents(state: GraphState) -> Dict[str, Any]:
    '''
    Determine whether the retrieved documents are relevant to the question
    If not relevant set it for web search

    :param state: The current graph state
    :return: Filter out irrelevant document and updated web_search state
    '''
    print("*******************Node : Grade Documents**************")
    question=state["question"]
    documents= state["documents"]
    web_search=False
    filtered_docs=[]
   
    for d in documents:
        score=retrieval_grader.invoke(
            {"question":question,"document":d.page_content}
        )
        grade=score.binary_score

        if grade.lower()=='yes':
            filtered_docs.append(d)
        else:
            web_search=True
            continue
    print()
    return {"documents":filtered_docs, "question":question,"web_search":web_search}