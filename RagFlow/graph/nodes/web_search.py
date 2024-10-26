from typing import Any, Dict

from langchain.chains.hyde.prompts import web_search
from langchain.schema import Document
from langchain_community.tools.tavily_search import TavilySearchResults
from RagFlow.graph.state import  GraphState
from dotenv import load_dotenv
load_dotenv()

web_search_tool=TavilySearchResults(max_results=5)

def tavily_web_search(state: GraphState)-> Dict[str, Any]:
    print("*******************Node : Web Search**************")
    question=state["question"]
    websearch=state['web_search']
    documents=state['documents']

    tavily_result= web_search_tool.invoke({"query":question})
    joined_tavily_result="\n".join(
        [
            result["content"] for result in tavily_result
        ]
    )
    web_result=Document(page_content=joined_tavily_result)
    if documents is not None:
        documents.append(web_result)
    else:
        documents=[web_result]
    return {"documents":documents,"question":question}