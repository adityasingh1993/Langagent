from datetime import datetime

from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser, PydanticToolsParser
from  langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


from reflexion.schema import AnswerQuestion

parser=JsonOutputToolsParser(return_id=True)
parser_pydantic= PydanticToolsParser(tools=[AnswerQuestion])
actor_prompt_template= ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are expert researcher.
            Current time: {time}
            1. {first_instruction}
            2. Reflect and critique your answer. Be severe to maximize improvement.
            3. Recommend search queries to research information and improve your answers
            """
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system","Answer the user's question above using required format")
    ]
).partial(time=lambda:datetime.now().isoformat())


first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer."
)

# first_responder= first_responder_prompt_template | llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion")
