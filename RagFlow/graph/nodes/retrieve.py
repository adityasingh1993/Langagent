
from typing import  Any, Dict

from typer.cli import state

from RagFlow.graph.state import GraphState
from RagFlow.ingestion.data_ingestion import Ingestion

class StateRetrieve():
    def __init__(self):
        self.ingestor=Ingestion()
        self.ingestor_retieve=self.ingestor.get_retriever()
    def retrieve(self,state: GraphState):
        print("*******************Node : Retrieve**************")
        print("----Retrieve----")
        print(state)
        question = state['question']
        documents=self.ingestor_retieve.invoke(question)
        return  {"documents":documents, "question":question}

