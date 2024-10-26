from pprint import pprint

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from  langchain_openai import ChatOpenAI
from reflexion.chains import first_responder_prompt_template, parser_pydantic
from reflexion.schema import AnswerQuestion

load_dotenv()

llm= ChatOpenAI()
if __name__=="__main__":
    human_message= HumanMessage(
        content="Write about AI-Powered SOC/autonomous soc problem domain,"
        " list startups that do that and raised capital"
    )

    chain= (first_responder_prompt_template|
            llm.bind_tools(tools=[AnswerQuestion], tool_choice='AnswerQuestion')
            | parser_pydantic
            )
    res = chain.invoke(input={"messages":[human_message]})
    pprint(res)

