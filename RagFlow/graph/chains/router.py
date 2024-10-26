from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_openai import ChatOpenAI

class RouteQuery(BaseModel):
    datasource: Literal["vectorstore","websearch"]= Field(
        description="Given a user question choose to route it to web search or a vectorscore"
    )

llm=ChatOpenAI()
structure_llm_router=llm.with_structured_output(RouteQuery)

system="""
You are an expert at routing user question to a vectorstore or web search.
The vectorstore contain the document related to agents, prompt engineering and adversarial attacks
Use vectorstore for question on these topics. For all else, use web search
"""

route_prompt=ChatPromptTemplate.from_messages([
    ("system",system),
    ("human","{question}")
])

question_router=route_prompt|structure_llm_router