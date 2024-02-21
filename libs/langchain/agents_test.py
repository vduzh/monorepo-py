import unittest

from dotenv import load_dotenv
from langchain.agents import tool, AgentExecutor
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_core.agents import AgentFinish
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.utils.function_calling import format_tool_to_openai_function

from libs.langchain.model import get_chat_model

load_dotenv()


# function name is also used by LLM to find a function
@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    # """use this tool when you need to calculate the length of a car using its name."""
    return len(word)


# function name is also used by LLM to find a function
@tool
def get_product_calories(product: str) -> int:
    """Calculates the amount of calories of the product."""
    # """use this tool when you need to calculate the number of calories the products contains."""
    # """use this tool when you need to calculate the price of the product."""
    return len(product * 100)


class TestTemplate(unittest.TestCase):

    def test_duck_duck_go_tool(self):
        search_tool = DuckDuckGoSearchRun()
        result = search_tool.run("Manchester United vs Luton town match summary")
        # print("DuckDuckGoSearchRun:result", result)

    def test_simple_agent(self):
        tools = [DuckDuckGoSearchRun()]
        agent_executor = create_conversational_retrieval_agent(
            get_chat_model(),
            tools,
            verbose=True)

        result = agent_executor({"input": "Manchester United vs Luton town match summary"})
        # print("simple_agent:", result["output"])

    def test_build_agent_from_scratch_with_custom_executor(self):
        # create the prompt for the agent
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a very powerful assistant but not great at calculating word lengths.",
                ),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        # create tools
        tools = {
            "get_word_length": get_word_length,
            "get_product_calories": get_product_calories,
        }
        # load the language model
        llm = get_chat_model()
        # bind tools to the model
        llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in list(tools.values())])

        # create an agent as a chain
        agent = (
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"]),
                }
                | prompt
                | llm_with_tools
                | OpenAIFunctionsAgentOutputParser()
        )

        # write a runtime for the agent
        user_inputs = [
            "how many letters in the word educa?",
            "How fatty is a croissant? Return the result as a number."
        ]
        for user_input in user_inputs:
            intermediate_steps = []
            while True:
                # the next action to take
                agent_action = agent.invoke({
                    "input": user_input,
                    "intermediate_steps": intermediate_steps
                })
                print("agent_action:", type(agent_action))

                if isinstance(agent_action, AgentFinish):
                    final_resul = agent_action.return_values["output"]
                    print("final_result:", final_resul)
                    break
                else:
                    print(f"TOOL NAME: {agent_action.tool}")
                    print(f"TOOL INPUT: {agent_action.tool_input}")
                    selected_tool = tools[agent_action.tool]
                    print(f"TOOL SELECTED: {selected_tool}")
                    observation = selected_tool.run(agent_action.tool_input)
                    print("observation:", observation)
                    intermediate_steps.append((agent_action, observation))

    def test_build_agent_from_scratch_with_agent_executor(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a very powerful assistant but not great at calculating word lengths.",
                ),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        tools = [get_word_length, get_product_calories]
        llm_with_tools = get_chat_model().bind(functions=[format_tool_to_openai_function(t) for t in tools])

        agent = (
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"]),
                }
                | prompt
                | llm_with_tools
                | OpenAIFunctionsAgentOutputParser()
        )

        user_inputs = [
            "How many letters in the word educa? Return the result as a number.",
            "How fatty is a croissant? Return the result as a number."
        ]
        for user_input in user_inputs:
            agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
            out_dict = agent_executor.invoke({"input": user_input})
            print("res:", out_dict["output"])

    #
    # def test_shell_tool(self):
    #     shell_tool = ShellTool()
    #     print(shell_tool.description)
    #
    #     result = shell_tool.run({"commands": ["echo 'Hello World!'", "time"]})
    #     # print(result)

    # def test_google_search(self):
    #     search = GoogleSearchAPIWrapper()
    #
    #     search_tool = Tool(
    #         name="Intermediate Answer",
    #         description="Search google for recent results",
    #         func=search.run
    #     )
    #
    #     google_serach_agent = initialize_agent(
    #         agent="self-ask-with-search",
    #         tools=[search_tool],
    #         llm=get_chat_model(),
    #         verbose=True,
    #         max_iterations=10
    #     )
    #
    #     res = google_serach_agent.run("The news about langchain")
    #     print(res)

    # def test_retrival_agent(self):
    #     # create a retriever over some data of our own.
    #     loader = WebBaseLoader("https://docs.smith.langchain.com/")
    #     docs = loader.load()
    #     vector = FAISS.from_documents(
    #         RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs),
    #         get_embeddings()
    #     )
    #     retriever = vector.as_retriever()
    #
    #     retriever_tool = create_retriever_tool(
    #         retriever,
    #         "langsmith_search",
    #         "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
    #     )
    #
    #     # create a list of tools
    #     tools = [retriever_tool]
    #
    #     # create agent
    #     agent_executor = create_conversational_retrieval_agent(get_chat_model(), tools, verbose=True)
    #
    #     q = "What is LangSmith?"
    #     result = agent_executor({"input": q})
    #     print("retrival_agent:", result["output"])

    # def test_define_tools(self):
    #     # create search tool
    #     search_tool = TavilySearchResults()
    #     # res = search_tool.invoke("what is the weather in SF")
    #
    #     # create a retriever over some data of our own.
    #     loader = WebBaseLoader("https://docs.smith.langchain.com/")
    #     docs = loader.load()
    #     vector = FAISS.from_documents(
    #         RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs),
    #         get_embeddings()
    #     )
    #     retriever = vector.as_retriever()
    #     # res = retriever.get_relevant_documents("how to upload a dataset")[0]
    #
    #     retriever_tool = create_retriever_tool(
    #         retriever,
    #         "langsmith_search",
    #         "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
    #     )
    #     # print(retriever_tool)
    #
    #     # create a list of tools
    #     tools = [search_tool, retriever_tool]
    #
    #     # create agent
    #     llm = get_chat_model()
    #
    #     # Get the prompt to use - you can modify this!
    #     prompt = hub.pull("hwchase17/openai-functions-agent")
    #     print(prompt.messages)


if __name__ == '__main__':
    unittest.main()
