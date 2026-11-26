"""
==========================================================
Version 1 - Production LangGraph Agent
==========================================================

This project demonstrates:

1. LangGraph StateGraph
2. MessagesState
3. Tool Calling
4. ToolNode
5. Conditional Routing
6. Gemini Integration

Memory is NOT included yet.
RAG is NOT included yet.

Those will be added in future versions.

==========================================================
"""

# ==========================================================
# Imports
# ==========================================================

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import HumanMessage

from langchain_core.tools import tool

from langgraph.graph import (
    StateGraph,
    MessagesState,
    START,
    END,
)

from langgraph.prebuilt import (
    ToolNode,
    tools_condition,
)


# ==========================================================
# Load Environment Variables
# ==========================================================

# Loads GOOGLE_API_KEY from .env file
load_dotenv()


# ==========================================================
# Create Gemini LLM
# ==========================================================

"""
We intentionally keep the original LLM separate.

Later, we create another instance with bound tools.

This keeps the architecture flexible.
"""

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)


# ==========================================================
# Tool Definitions
# ==========================================================

@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression.

    Example:

    5 + 10

    40 / 8

    50 * 4
    """

    return str(eval(expression))


@tool
def reverse_text(text: str) -> str:
    """
    Reverse any text.
    """

    return text[::-1]


@tool
def word_counter(text: str) -> str:
    """
    Count total words inside a text.
    """

    return str(len(text.split()))


# ==========================================================
# Tool List
# ==========================================================

"""
Every tool is stored inside one list.

Production agents may contain
20+
50+
even 100+ tools.

That's why LangGraph accepts a list.
"""

tools = [

    calculator,

    reverse_text,

    word_counter,

]


# ==========================================================
# Bind Tools
# ==========================================================

"""
bind_tools()

DOES NOT execute tools.

It simply tells the LLM

"These tools are available."

The model can now decide
whether it wants to call them.
"""

llm_with_tools = llm.bind_tools(tools)


# ==========================================================
# Chatbot Node
# ==========================================================

"""
Every node receives State.

Every node returns State.

The reducer inside MessagesState
will automatically append
new messages.

It will NOT overwrite history.
"""

def chatbot(state: MessagesState):

    response = llm_with_tools.invoke(

        state["messages"]

    )

    return {

        "messages": [

            response

        ]

    }


# ==========================================================
# Tool Node
# ==========================================================

"""
ToolNode is responsible ONLY for

1. Reading tool requests

2. Executing tools

3. Returning ToolMessage

It NEVER talks directly to the user.
"""

tool_node = ToolNode(tools)


# ==========================================================
# Build Graph
# ==========================================================

graph = StateGraph(MessagesState)


# ==========================================================
# Register Nodes
# ==========================================================

graph.add_node(

    "chatbot",

    chatbot,

)

graph.add_node(

    "tools",

    tool_node,

)


# ==========================================================
# START Edge
# ==========================================================

"""
Every execution begins
from START.

START

↓

chatbot
"""

graph.add_edge(

    START,

    "chatbot",

)
# ==========================================================
# Conditional Routing
# ==========================================================

"""
After every chatbot response, LangGraph must decide:

1. Should the conversation END?

OR

2. Should it execute a Tool?

This decision is made by tools_condition().

Internally it checks the last AIMessage.

If tool_calls exist:

    chatbot --> tools

Otherwise:

    chatbot --> END
"""

graph.add_conditional_edges(

    "chatbot",

    tools_condition,

)


# ==========================================================
# Tool → Chatbot
# ==========================================================

"""
After a tool finishes execution,
its result is stored as a ToolMessage.

The LLM must see that ToolMessage
before generating the final answer.

Therefore we return back to chatbot.

Flow:

Chatbot

↓

ToolNode

↓

Chatbot

↓

END
"""

graph.add_edge(

    "tools",

    "chatbot",

)


# ==========================================================
# Compile Graph
# ==========================================================

"""
Compile converts the graph definition
into an executable application.
"""

app = graph.compile()


# ==========================================================
# Interactive Chat
# ==========================================================

def main():

    print("=" * 60)
    print("LangGraph Version 1")
    print("=" * 60)

    print("\nType 'exit' to quit.\n")

    conversation = []

    while True:

        user_input = input("You : ")

        if user_input.lower() in {

            "exit",

            "quit",

            "q"

        }:
            print("\nGood Bye!\n")
            break

        # --------------------------------------------------
        # Add Human Message
        # --------------------------------------------------

        conversation.append(

            HumanMessage(
                content=user_input
            )

        )

        # --------------------------------------------------
        # Invoke Graph
        # --------------------------------------------------

        result = app.invoke(

            {

                "messages": conversation

            }

        )

        # --------------------------------------------------
        # Save Updated Conversation
        # --------------------------------------------------

        conversation = result["messages"]

        # --------------------------------------------------
        # Last Message
        # --------------------------------------------------

        final_response = conversation[-1]

        print()

        print("Assistant :")

        print(final_response.content)

        print()

        print("-" * 60)

        print()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    main()