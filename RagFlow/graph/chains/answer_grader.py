from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI

from RagFlow.graph.chains.retrieval_grader import system


class GradeAnswer(BaseModel):
    binary_score:bool= Field(description="IS answer address the question , 'yes' or 'no'")

llm= ChatOpenAI(temperature=0)

structure_llm_grader= llm.with_structured_output(GradeAnswer)
system = """You are a  grader assessing whether an answer addresses / resolve a question \n
Give a binary score 'yes' or 'no'. 'Yes' means that the answer resolves the question  
"""

answer_prompt= ChatPromptTemplate.from_messages(
    [
        ("system",system),
        ("human","User question: \n\n {question} \n\n LLM generation: {generation}"),
    ]
)

answer_grader: RunnableSequence = answer_prompt | structure_llm_grader