from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from reflection.chains import generate_chain
print("============generation chain========")
llm=ChatOpenAI()
prompt=hub.pull("rlm/rag-prompt")
generate_chain = prompt|llm|StrOutputParser()
print(generate_chain)
print("==========End Generation Chain=======s")