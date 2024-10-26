from pprint import pprint

from dotenv import load_dotenv

from RagFlow.graph.chains.retrieval_grader import retrieval_grader, GradeDocument
from RagFlow.graph.chains.generation import generate_chain
from RagFlow.graph.nodes import generate
from RagFlow.graph.chains.hallucination_grader import  hallucination_grader
from RagFlow.graph.chains.answer_grader import  answer_grader
from RagFlow.graph.chains.router import question_router

load_dotenv()
from RagFlow.ingestion.data_ingestion import Ingestion
def test_foo():
    assert 1==1

def test_retrival_grader_answer_yes():
    ingest=Ingestion()
    retriever=ingest.get_retriever()
    question='agent memory'
    docs= retriever.invoke(question)
    doc_txt =docs[1].page_content
    res:GradeDocument= retrieval_grader.invoke({"question":question,"document":doc_txt})
    assert res.binary_score=='yes'

def test_retrival_grader_answer_no():
    ingest=Ingestion()
    retriever=ingest.get_retriever()
    question='pizza making'
    docs= retriever.invoke(question)
    doc_txt =docs[1].page_content
    res:GradeDocument= retrieval_grader.invoke({"question":question,"document":doc_txt})
    assert res.binary_score=='no'

def test_generation_chaib():
    ingest = Ingestion()
    retriever = ingest.get_retriever()
    question = 'agent memory'
    docs = retriever.invoke(question)
    generation = generate_chain.invoke({"context":docs,"question":question})
    pprint(generation)


# def test_answer_gradr_yes():
#     ingest = Ingestion()
#     retriever = ingest.get_retriever()
#     question = 'agent memory'
#     docs=retriever.invoke(question)
#     generation=generate_chain.invoke({
#         "context": docs, "question": question
#     })
#     res = answer_grader.invoke(
#         {"documents": docs, "generation": generation}
#     )
#     assert res.binary_score.lower()=='yes'

def test_hallucination_gradr_yes():
    ingest = Ingestion()
    retriever = ingest.get_retriever()
    question = 'agent memory'
    docs=retriever.invoke(question)
    generation=generate_chain.invoke({
        "context": docs, "question": question
    })
    res = hallucination_grader.invoke(
        {"documents": docs, "generation": generation}
    )
    assert res.binary_score

def test_hallucination_gradr_no():
    ingest = Ingestion()
    retriever = ingest.get_retriever()
    question = 'agent memory'
    docs=retriever.invoke(question)
    generation=generate_chain.invoke({
        "context": docs, "question": question
    })
    res = hallucination_grader.invoke(
        {"documents": docs, "generation": "mai pizza khayga"}
    )
    assert res.binary_score==False

def test_vectorstore_route():
    question = 'agent memory'
    res=question_router.invoke({"question":question})
    assert res.datasource=='vectorstore'
def test_websearch_route():
    question = 'pizza story'
    res=question_router.invoke({"question":question})
    assert res.datasource=='websearch'