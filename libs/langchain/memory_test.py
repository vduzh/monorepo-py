import unittest
from pprint import pprint

from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.chains import LLMChain, ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferWindowMemory, ConversationEntityMemory, ConversationSummaryMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.utilities.google_search import GoogleSearchAPIWrapper
from langchain_core.memory import BaseMemory
from langchain_core.messages import BaseMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, \
    HumanMessagePromptTemplate
from langchain_core.tools import Tool

from libs.langchain.vector_stores import build_vector_store_from_text_file
from model import get_llm, get_chat_model


class TestMemory(unittest.TestCase):

    @staticmethod
    def _create_memory(memory_key="history", return_messages=False) -> BaseMemory:
        memory = ConversationBufferMemory(memory_key=memory_key, return_messages=return_messages)
        memory.chat_memory.add_user_message("hi!")
        memory.chat_memory.add_ai_message("what's up?")
        return memory

    def test_create_memory(self):
        memory = self._create_memory()
        pprint(memory)

    def test_chat_message_history(self):
        history = ChatMessageHistory()

        history.add_user_message("hi!")
        history.add_ai_message("what's up?")

        # pprint(history)

        # assert the result
        self.assertEqual(len(history.messages), 2)

    def test_extract_messages_as_string_in_variables(self):
        memory_variables_dict = self._create_memory().load_memory_variables({})
        self.assertEqual({'history': "Human: hi!\nAI: what's up?"}, memory_variables_dict)

        memory_variables_dict = self._create_memory(memory_key="chat_history").load_memory_variables({})
        self.assertEqual({'chat_history': "Human: hi!\nAI: what's up?"}, memory_variables_dict)

    def test_extract_messages_as_list_of_messages_in_variables(self):
        memory_variables_dict = self._create_memory(return_messages=True).load_memory_variables({})
        messages = memory_variables_dict.get("history")

        self.assertTrue(all(isinstance(obj, BaseMessage) for obj in messages))

    def test_conversation_buffer_memory(self):
        memory = ConversationBufferMemory()
        memory.save_context({"input": "hi!"}, {"output": "what's up?"})
        # pprint(memory)

        # assert the result
        memory_variables_dict = memory.load_memory_variables({})
        self.assertEqual({'history': "Human: hi!\nAI: what's up?"}, memory_variables_dict)

    def test_conversation_buffer_window_memory(self):
        memory = ConversationBufferWindowMemory(k=1)
        memory.save_context({"input": "hi!"}, {"output": "what's up?"})
        memory.save_context({"input": "mot much you"}, {"output": "not much"})
        # pprint(memory)

        # assert the result
        self.assertEqual(4, len(memory.chat_memory.messages))

        memory_variables_dict = memory.load_memory_variables({})
        self.assertEqual({'history': "Human: mot much you\nAI: not much"}, memory_variables_dict)

    def test_conversation_chain_with_conversation_buffer_memory(self):
        conversation = ConversationChain(
            llm=get_llm(),
            verbose=True,
            memory=ConversationBufferMemory()
        )

        text = conversation.predict(input="Hi there!")
        print("step #1:", text)

        text = conversation.predict(input="I'm doing well! Just having a conversation with an AI.")
        print("step #2:", text)

        text = conversation.predict(input="Tell me about yourself.")
        print("step #3:", text)

    def test_conversation_chain_with_conversation_buffer_window_memory(self):
        conversation = ConversationChain(
            llm=get_llm(),
            verbose=True,
            memory=ConversationBufferWindowMemory(k=2)
        )

        text = conversation.predict(input="Hi, what's up?")
        print("step #1:", text)

        text = conversation.predict(input="Is it going well?")
        print("step #2:", text)

    def test_conversation_summary_memory(self):
        # https://python.langchain.com/docs/modules/memory/types/summary
        memory = ConversationSummaryMemory()
        raise NotImplementedError()


    def test_entity_not_finished_yet(self):
        memory = ConversationEntityMemory(llm=get_llm())
        _input = {"input": "Deven & Sam are working on a hackathon project"}
        memory_variables_dict = memory.load_memory_variables(_input)
        pprint(memory_variables_dict)

        memory.save_context(
            _input,
            {'output': 'That sounds like a great project! What kind of project are they working on?'}
        )
        memory_variables_dict = memory.load_memory_variables({"input": 'who is Sam'})
        pprint(memory_variables_dict)

    def test_llm(self):
        # create prompt template
        template = """
        You are a nice chatbot having a conversation with a human.

        Previous conversation:
        {chat_history}

        New human question: {question}
        Response:
        """
        prompt = PromptTemplate.from_template(template)

        # create memory
        memory = ConversationBufferMemory(memory_key="chat_history")

        # create chain
        chain = LLMChain(
            llm=get_llm(),
            prompt=prompt,
            verbose=True,
            memory=memory
        )

        # we just pass in the `question` variables - `chat_history` gets populated by memory
        out_dict = chain({"question": "hi"})
        pprint(out_dict)

        # assert the result
        self.assertEqual("", out_dict["chat_history"])
        self.assertEqual("hi", out_dict["question"])
        self.assertNotEqual("", out_dict["text"])

    def test_chat(self):
        # create prompt template
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("You are a nice chatbot having a conversation with a human."),
            # The `variable_name` here is what must align with memory
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}")
        ])

        # create memory
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # create chain
        chain = LLMChain(
            llm=get_chat_model(),
            prompt=prompt,
            verbose=True,
            memory=memory
        )

        # we just pass in the `question` variables - `chat_history` gets populated by memory
        out_dict = chain({"question": "hi"})
        pprint(out_dict)

        # assert the result
        self.assertEqual(len(out_dict["chat_history"]), 2)
        self.assertEqual("hi", out_dict["question"])
        self.assertNotEqual("", out_dict["text"])

    def test_memory_in_multi_input_chain(self):
        # build a vector store from the state_of_the_union.txt file in the data folder
        vectorstore = build_vector_store_from_text_file()

        query = "What did the president say about Justice Breyer"
        docs = vectorstore.similarity_search(query)
        # pprint(docs)

        # create prompt
        template = """You are a chatbot having a conversation with a human.

        Given the following extracted parts of a long document and a question, create a final answer.

        {context}

        {chat_history}
        Human: {human_input}
        Chatbot:"""

        prompt = PromptTemplate(input_variables=["chat_history", "human_input", "context"], template=template)

        # init memory
        memory = ConversationBufferMemory(memory_key="chat_history", input_key="human_input")

        # create a chain
        chain = load_qa_chain(get_llm(), chain_type="stuff", memory=memory, prompt=prompt, verbose=True)

        query = "What did the president say about Justice Breyer"
        out_dict = chain({"input_documents": docs, "human_input": query}, return_only_outputs=True)

        pprint(out_dict)

    def test_memory_in_agent(self):
        # create a search tool
        search = GoogleSearchAPIWrapper()
        tools = [
            Tool(
                name="Search",
                func=search.run,
                description="useful for when you need to answer questions about current events",
            )
        ]

        # build prompt
        prefix = """
        Have a conversation with a human, answering the following questions as best you can. 
        You have access to the following tools:
        """
        suffix = """
        Begin!"

        {chat_history}
        Question: {input}
        {agent_scratchpad}
        """

        prompt = ZeroShotAgent.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=["input", "chat_history", "agent_scratchpad"],
        )

        # init memory
        memory = ConversationBufferMemory(memory_key="chat_history")

        # construct the LLMChain, with the Memory
        llm_chain = LLMChain(llm=get_llm(), prompt=prompt)

        # create the agent
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
        agent_chain = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, verbose=True, memory=memory
        )

        out_dict = agent_chain.run(input="How many people live in canada?")
        print("step 1:", out_dict)

        # the agent remembered that the previous question was about Canada,
        # and properly asked Google Search what the name of Canada’s national anthem was.
        out_dict = agent_chain.run(input="what is their national anthem called?")
        print("step 2:", out_dict)


if __name__ == '__main__':
    unittest.main()
