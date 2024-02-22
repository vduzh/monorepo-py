import unittest
from pprint import pprint

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import tool, AgentExecutor, create_openai_functions_agent, create_openai_tools_agent, \
    create_json_chat_agent, create_structured_chat_agent
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.agents import AgentFinish
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.utils.function_calling import format_tool_to_openai_function

from libs.langchain.model import get_chat_model

load_dotenv()


@tool
def get_word_length(word: str) -> int:
    """use this tool when you need to calculate the length of a word."""
    return len(word)


@tool
def get_product_calories(product: str) -> int:
    """use this tool when you need to calculate the number of calories the products contains."""
    return len(product * 100)


# class CaloriesCalculatorTool(BaseTool):
#     name = "Calories calculator"
#     description = "use this tool when you need to calculate the amount of calories a product contains."
#
#     def _run(self, product: str) -> int:
#         return len(product * 100)
#
#     def _arun(self, product: str) -> int:
#         raise NotImplementedError("This tool does not support async")


class TestAgents(unittest.TestCase):

    def test_simple_agent(self):
        tools = [DuckDuckGoSearchRun()]
        agent_executor = create_conversational_retrieval_agent(
            get_chat_model(),
            tools,
            verbose=True)

        result = agent_executor({"input": "Manchester United vs Luton town match summary"})
        print("simple_agent:", result["output"])

    def test_build_agent_from_scratch_with_custom_executor(self):
        # create the prompt for the agent
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a very powerful assistant but not great at calculating word lengths.",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
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
                    "chat_history": lambda х: х["chat_history"],
                }
                | prompt
                | llm_with_tools
                | OpenAIFunctionsAgentOutputParser()
        )

        # write a runtime (agent executor) for the agent
        user_inputs = [
            "how many letters in the word educa?",
            "How fatty is a croissant? Return the result as a number."
        ]
        for user_input in user_inputs:
            chat_history = []
            intermediate_steps = []
            while True:
                # the next action to take
                agent_action = agent.invoke({
                    "input": user_input,
                    "intermediate_steps": intermediate_steps,
                    "chat_history": chat_history
                })
                print("agent_action:", type(agent_action))

                if isinstance(agent_action, AgentFinish):
                    final_result_str = agent_action.return_values["output"]
                    print("final_result:", final_result_str)
                    chat_history.extend([HumanMessage(content=user_input), AIMessage(content=final_result_str)])
                    print("chat_history:", chat_history)
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
                MessagesPlaceholder(variable_name="chat_history"),
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
                    "chat_history": lambda х: х["chat_history"],
                }
                | prompt
                | llm_with_tools
                | OpenAIFunctionsAgentOutputParser()
        )

        user_inputs = [
            "How many letters in the word educa? Return the result as a number.",
            "How fatty is a croissant? Return the result as a number."
        ]
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        for user_input in user_inputs:
            chat_history = []
            out_dict = agent_executor.invoke({"input": user_input, "chat_history": chat_history})
            result_str = out_dict["output"]
            print("result:", result_str)
            chat_history.extend([HumanMessage(content=user_input), AIMessage(content=result_str)])
            print("chat_history:", chat_history)

    def test_openai_functions_agent_deprecated(self):
        # initialize tools
        tools = [TavilySearchResults(max_results=1)]

        # Create Agent
        # get the prompt to use - you can modify this!
        prompt = hub.pull("hwchase17/openai-functions-agent")
        # get LLM that will drive the agent
        llm = get_chat_model()
        # construct the OpenAI Functions agent
        agent = create_openai_functions_agent(llm, tools, prompt)

        # Run Agent
        # create an agent executor by passing in the agent and tools
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        res_str = agent_executor.invoke({"input": "what is LangChain?"})
        pprint(res_str["output"])

        # Run Agent with chat history
        res_str = agent_executor.invoke(
            {
                "input": "what's my name?",
                "chat_history": [
                    HumanMessage(content="hi! my name is bob"),
                    AIMessage(content="Hello Bob! How can I assist you today?"),
                ],
            }
        )
        pprint(res_str["output"])

    def test_openai_tools_agent(self):
        # initialize tools
        tools = [TavilySearchResults(max_results=1)]

        # create agent
        prompt = hub.pull("hwchase17/openai-tools-agent")
        llm = get_chat_model()
        agent = create_openai_tools_agent(llm, tools, prompt)

        # run agent
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        res_str = agent_executor.invoke({"input": "what is LangChain?"})
        pprint(res_str["output"])

        # Run Agent with chat history
        res_str = agent_executor.invoke(
            {
                "input": "what's my name? Don't use tools to look this up unless you NEED to",
                "chat_history": [
                    HumanMessage(content="hi! my name is bob"),
                    AIMessage(content="Hello Bob! How can I assist you today?"),
                ],
            }
        )
        pprint(res_str["output"])

    def test_json_chat_agent(self):
        # initialize tools
        tools = [TavilySearchResults(max_results=1)]

        # create agent
        prompt = hub.pull("hwchase17/react-chat-json")
        llm = get_chat_model()
        agent = create_json_chat_agent(llm, tools, prompt)

        # run agent
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

        res_str = agent_executor.invoke({"input": "what is LangChain?"})
        pprint(res_str["output"])

        # Run Agent with chat history
        res_str = agent_executor.invoke(
            {
                "input": "what's my name?",
                "chat_history": [
                    HumanMessage(content="hi! my name is bob"),
                    AIMessage(content="Hello Bob! How can I assist you today?"),
                ],
            }
        )
        pprint(res_str["output"])

    def test_structured_chat_agent(self):
        # initialize tools
        tools = [TavilySearchResults(max_results=1)]

        # create agent
        prompt = hub.pull("hwchase17/structured-chat-agent")
        llm = get_chat_model()
        agent = create_structured_chat_agent(llm, tools, prompt)

        # run agent
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

        res_str = agent_executor.invoke({"input": "what is LangChain?"})
        pprint(res_str["output"])

        # Run Agent with chat history
        res_str = agent_executor.invoke(
            {
                "input": "what's my name? Do not use tools unless you have to",
                "chat_history": [
                    HumanMessage(content="hi! my name is bob"),
                    AIMessage(content="Hello Bob! How can I assist you today?"),
                ],
            })
        pprint(res_str["output"])

    #

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


if __name__ == '__main__':
    unittest.main()
