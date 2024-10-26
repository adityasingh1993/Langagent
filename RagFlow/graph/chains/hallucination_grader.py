from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field

from RagFlow.graph.chains.retrieval_grader import system

llm=ChatOpenAI(temperature=0)

class GradeHallucination(BaseModel):
    binary_score:bool= Field(description="Score for grading hallucination in yes or no")

structured_llm_grader = llm.with_structured_output(GradeHallucination)
system=""" You are a grader assesing whether an LLM generation is grounded in / supported by the given set of documents.
Give a binary score 'yes' or 'no'. 'Yes' means the answer is grounded / supported by the set of documents 
"""

hallucination_prompt=ChatPromptTemplate.from_messages(
[    ("system", system),
    ("human", "User question: \n\n {documents} \n\n LLM generation: {generation}")
])
hallucination_grader: RunnableSequence = hallucination_prompt | structured_llm_grader