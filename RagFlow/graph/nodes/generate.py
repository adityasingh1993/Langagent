from typing import Any, Dict
from RagFlow.graph.chains.generation import generate_chain
from RagFlow.graph.state import GraphState
def generate(state: GraphState):
    print("*******************Node : Generate**************")
    question=state['question']
    documents=state['documents']
    generation= generate_chain.invoke({"context":documents,"question":question})
    return {"documents":documents, "question":question, "generation":generation}