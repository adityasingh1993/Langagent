from pydantic import BaseModel
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
llm= ChatOpenAI()
print("============Retrieval Grader========")
class GradeDocument(BaseModel):
    binary_score: str= Field()

structure_llm_grader= llm.with_structured_output(GradeDocument)

system=""" You are a grader assessing relevance of a retrieved document to a user question.\n
If the document contains keyword(s) or semantic meaning related to the question, grade it as a relevent.
Give a binary score 'yes' or 'no' score to indicate whether the document is relevant or not

"""

grade_prompt= ChatPromptTemplate.from_messages([
    ("system",system),
    ("human",'Retrieved documents: \n\n {document} \n\n user_question: {question}')
])
retrieval_grader=grade_prompt|structure_llm_grader
print("====================Retrieval Ender==============")