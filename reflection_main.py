from distutils.command.build import build
from pprint import pprint
from typing import List, Sequence
from dotenv import load_dotenv
from tenacity import retry

load_dotenv()
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
# Press the green button in the gutter to run the script.
from reflection.chains import generate_chain, reflect_chain
REFLECT="reflect"
GENERATE="generate"

def generation_node(state: Sequence[BaseMessage]):
    return  generate_chain.invoke({"messages":state})

def reflection_node(messages: Sequence[BaseMessage]):
    res=reflect_chain.invoke({"messages":messages})
    return [HumanMessage(content=res.content)]

builder=MessageGraph()
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(GENERATE)

def should_continue(state: List[BaseMessage]):
    if len(state)>6:
        return END
    return  REFLECT

builder.add_conditional_edges(GENERATE, should_continue)
builder.add_edge(REFLECT,GENERATE)
graph=builder.compile()
# print(graph.get_graph().draw_mermaid())
print(graph.get_graph().print_ascii())
if __name__ == '__main__':
    print('PyCharm')
    # inputs= HumanMessage(content="""
    # Make this tweet better
    # @LangChainAI
    # — newly Tool Calling feature is seriously underrated.
    # After a long wait, it's  here- making the implementation of agents across different models with function calling - super easy.
    #
    # Made a video covering their newest blog post
    # """)
    inputs=HumanMessage(content="""
    Make this tweet better
    @orry
    Orry is just an wonderful licking influencer, who does nothing
    """)
    response = graph.invoke(inputs)
    pprint(response)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
