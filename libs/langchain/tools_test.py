import unittest
from pprint import pprint
from typing import Type, Optional

from dotenv import load_dotenv
from langchain.agents import tool
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_community.tools.file_management import MoveFileTool
from langchain_community.tools.shell import ShellTool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_core.callbacks import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool, StructuredTool
from langchain_core.utils.function_calling import convert_to_openai_function
from pydantic.v1 import BaseModel, Field

from libs.langchain.model import get_chat_model

load_dotenv()


class WikiInputs(BaseModel):
    """Inputs to the wikipedia tool."""

    query: str = Field(
        description="query to look up in Wikipedia, should be 3 or less words"
    )


@tool
def search(query: str) -> str:
    """Look up things online."""
    return "LangChain"


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


class WordInput(BaseModel):
    name: str = Field(description="should be a word")


# function name is also used by LLM to find a function
@tool("get_word_length", args_schema=WordInput, return_direct=True)
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    # """use this tool when you need to calculate the length of a car using its name."""
    return len(word)


# function name is also used by LLM to find a function
# @tool
# def get_product_calories(product: str) -> int:
#     """Calculates the amount of calories of the product."""
#     # """use this tool when you need to calculate the number of calories the products contains."""
#     # """use this tool when you need to calculate the price of the product."""
#     return len(product * 100)


class ProductInput(BaseModel):
    name: str = Field(description="should be the name of the product")


class CaloriesCalculatorTool(BaseTool):
    name = "calories_calculator"
    description = "use this tool when you need to calculate the amount of calories a product contains."
    args_schema: Type[BaseModel] = ProductInput

    def _run(self, name: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> int:
        """Use the tool."""
        return len(name * 100)

    def _arun(self, name: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> int:
        raise NotImplementedError("calories_calculator tool does not support async")


def say_hello(name: str) -> str:
    """Greets a person."""
    return f"Hello {name}!"


class TestTools(unittest.TestCase):
    def test_built_in_tool(self):
        api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
        search_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

        # wikipedia
        print("default name:", search_tool.name)

        # A wrapper around Wikipedia. Useful for when you need to answer general questions about people, places,
        # companies, facts, historical events, or other subjects. Input should be a search query.
        print("default description:", search_tool.description)

        # {'query': {'title': 'Query', 'type': 'string'}}
        print("default JSON schema of the inputs:", search_tool.args)

        # if the tool should return directly to the user
        print("return directly to the user:", search_tool.return_direct)

        # Call the tool with a dictionary input
        res_str = search_tool.run({"query": "langchain"})
        print("result of call #1:", res_str)
        # Call the tool with a single string input
        res_str = search_tool.run("langchain")
        print("result of call #2:", res_str)

    def test_customizing_built_in_tool(self):
        api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
        search_tool = WikipediaQueryRun(
            name="wiki-tool",
            description="look up things in wikipedia",
            args_schema=WikiInputs,
            api_wrapper=api_wrapper,
            return_direct=True,
        )

        print("default name:", search_tool.name)
        print("default description:", search_tool.description)
        print("default JSON schema of the inputs:", search_tool.args)
        print("return directly to the user:", search_tool.return_direct)

        res_str = search_tool.run("langchain")
        print("result of call:", res_str)

    def test_built_in_shell_tool(self):
        shell_tool = ShellTool()
        print(shell_tool.description)

        result = shell_tool.run({"commands": ["echo 'Hello World!'", "time"]})
        pprint(result)

    def test_built_in_duck_duck_go_tool(self):
        search_tool = DuckDuckGoSearchRun()
        result = search_tool.run("Manchester United vs Luton town match summary")
        # print("DuckDuckGoSearchRun:result", result)

    def test_built_in_tavily_search_results_tool(self):
        search_tool = TavilySearchResults(max_results=1)
        results = search_tool.run("what is LangChain?")
        print("TavilySearchResults:result", results[0]["content"])

    def test_custom_tool_with_tool_decorator(self):
        custom_tool = search

        print("default name:", custom_tool.name)
        print("default description:", custom_tool.description)
        print("default JSON schema of the inputs:", custom_tool.args)
        print("return directly to the user:", custom_tool.return_direct)

    def test_custom_tool_with_multiple_inputs(self):
        custom_tool = multiply

        print("default name:", custom_tool.name)
        print("default description:", custom_tool.description)
        print("default JSON schema of the inputs:", custom_tool.args)
        print("return directly to the user:", custom_tool.return_direct)

    def test_custom_tool_with_subclassing_base_tool(self):
        custom_tool = CaloriesCalculatorTool()

        print("default name:", custom_tool.name)
        print("default description:", custom_tool.description)
        print("default JSON schema of the inputs:", custom_tool.args)
        print("return directly to the user:", custom_tool.return_direct)

        res_str = custom_tool.run({"name": "lemon"})
        self.assertEqual(500, res_str)

        res_str = custom_tool.run("orange")
        self.assertEqual(600, res_str)

    def test_custom_tool_with_structured_tool_dataclass(self):
        custom_tool = StructuredTool.from_function(
            func=say_hello,
            name="Greeting",
            description="useful for when you need to somebody with its name",
        )

        print("default name:", custom_tool.name)
        print("default description:", custom_tool.description)
        print("default JSON schema of the inputs:", custom_tool.args)
        print("return directly to the user:", custom_tool.return_direct)

        res_str = custom_tool.run("John")
        self.assertEqual("Hello John!", res_str)

    def test_tools_as_openai_functions(self):
        tools = [MoveFileTool()]
        functions = [convert_to_openai_function(t) for t in tools]

        model = get_chat_model()
        ai_message = model.invoke([HumanMessage(content="move file foo to bar")], functions=functions)
        # pprint(ai_message)

    def test_tools_as_openai_functions_with_auto_bind(self):
        tools = [MoveFileTool()]
        model_with_functions = get_chat_model().bind_functions(tools)

        ai_message = model_with_functions.invoke([HumanMessage(content="move file foo to bar")])
        # pprint(ai_message)

    def test_tools_as_openai_functions_with_tool_choice(self):
        tools = [MoveFileTool()]
        model_with_tools = get_chat_model().bind_tools(tools)

        ai_message = model_with_tools.invoke([HumanMessage(content="move file foo to bar")])
        pprint(ai_message)

    def test_toolkit(self):
        raise NotImplementedError("test_toolkit is not implemented yet!")

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
