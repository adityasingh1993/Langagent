from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from posthog import personal_api_key


class Ingestion():
    def __init__(self,urls=[]):
        if len(urls)==0:
            self.urls=[
                "https://lilianweng.github.io/posts/2023-06-23-agent/",
                "https://truera.com/ai-quality-education/generative-ai-agents/what-are-llm-powered-autonomous-agents/"

            ]
        else:
            self.urls=urls
        self.chroma_path='./.chroma'

        self.embed=OpenAIEmbeddings()
        self.collection_name="rag-chroma"

    def load_data(self):
        docs=[WebBaseLoader(url).load() for url in self.urls]
        doc_list=[item for sublist in docs for item in sublist]
        char_splitter=CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        doc_splits= char_splitter.split_documents(doc_list)
        vectorscore=Chroma.from_documents(documents=doc_splits,
                                          collection_name="rag-chroma",
                                          embedding= self.embed,
                                          persist_directory=self.chroma_path,)


    def get_retriever(self):
        retriever=Chroma(
            collection_name=self.collection_name,
            persist_directory=self.chroma_path,
            embedding_function=self.embed

        ).as_retriever()
        return  retriever



