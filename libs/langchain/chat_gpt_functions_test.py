import json
import unittest

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, PromptTemplate
from langchain_core.tools import Tool

from libs.langchain.model import get_chat_model, get_llm


class TestChatGPTFunction(unittest.TestCase):

    def test_idea_with_any_model(self):
        llm = get_llm()

        # compose a prompt
        start_prompt_template = PromptTemplate.from_template("""
            You are a helpful assistant.
            
            You have access to the following tools:
                    
            - run_query: runs a sqlite query and returns the result. Accepts an argument of a sql as a string.
                    
            To use a tool always respond as JSON object with 2 fields but without json prefix:
            1. name - the name of tool to use
            2. argument - the argument to pass to the tool                   
                
            How many open orders so we have?                
        """)

        # build a chain
        chain = start_prompt_template | llm

        # invoke the chain
        res_text = chain.invoke({})

        print(res_text.strip())

        # encode the content as JSON
        content = json.loads(res_text)

        match content["name"]:
            # handle the run_query function
            case "run_query":
                # extract sql
                sql = content["argument"]

                def run_query(s: str):
                    return 93

                # call local function with arguments from ChatGPT
                count = run_query(sql)

                prompt_template = PromptTemplate.from_template(
                    start_prompt_template.template + "\n" +
                    "AI: " + res_text + "\n" +
                    "Human : " + str(count)
                )

                chain = prompt_template | llm
                response = chain.invoke({})
                print(response.content)
            case _:
                raise NotImplementedError("function is not implemented")

    def test_functions_from_scratch(self):
        chat_model = get_chat_model()

        # compose a prompt
        start_prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content="You are a helpful assistant"),
                HumanMessagePromptTemplate.from_template("""
                    You have access to the following tools:
                    
                    - run_query: runs a sqlite query and returns the result. Accepts an argument of a sql as a string.
                    
                    To use a tool always respond as JSON object with 2 fields but without json prefix:
                    1. name - the name of tool to use
                    2. argument - the argument to pass to the tool                   
                
                    How many open orders so we have?                
                """),
            ]
        )

        # build a chain
        chain = start_prompt_template | chat_model

        # invoke the chain
        res_msg = chain.invoke({})

        # encode the content as JSON
        content = json.loads(res_msg.content)

        match content["name"]:
            # handle the run_query function
            case "run_query":
                # extract sql
                sql = content["argument"]

                def run_query(s: str):
                    return 93

                # call local function with arguments from ChatGPT
                count = run_query(sql)

                prompt_template = ChatPromptTemplate.from_messages([
                    start_prompt_template,
                    res_msg,
                    HumanMessage(content=str(count))
                ])

                chain = prompt_template | chat_model
                response = chain.invoke({})
                print(response.content)
            case _:
                raise NotImplementedError("function is not implemented")

    def test_simple(self):
        def run_query(query):
            # logic to run a sql query
            return 93

        # the tool will be converted into a function description for OpenAI
        tool = Tool.from_function(
            name="execute_a_query",
            description="run a sqlite query",
            func=run_query
        )

        print("Testing bar")


if __name__ == '__main__':
    unittest.main()
