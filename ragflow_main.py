from dotenv import load_dotenv
load_dotenv()
from  RagFlow.ingestion.data_ingestion import  Ingestion
from RagFlow.graph.graph import  app
ingest=Ingestion()
ingest.load_data()
if __name__=='__main__':
    print("===RagFlow===")
    print(app.invoke(
        input={"question": "What is Pizza?"}
    ))