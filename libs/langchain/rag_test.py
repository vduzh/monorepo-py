import unittest

from langchain import hub
from langchain.chains import create_retrieval_chain, LLMChain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.tracers import ConsoleCallbackHandler

from libs.langchain.model import get_llm
from libs.langchain.vector_stores import get_file_vector_store


# https://python.langchain.com/docs/use_cases/question_answering/
class TestRetrievalAugmentedGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # build a vector store from the state_of_the_union.txt file in the data folder
        cls.vectorstore = get_file_vector_store()

    def test_rag_with_retrieval_chain(self):
        vector_store_retriever = self.vectorstore.as_retriever()

        prompt = hub.pull("langchain-ai/retrieval-qa-chat")

        combine_docs_chain = create_stuff_documents_chain(get_llm(), prompt)
        retrieval_chain = create_retrieval_chain(vector_store_retriever, combine_docs_chain)

        query = "What did the president say about Ketanji Brown Jackson?"
        out_dict = retrieval_chain.invoke(
            {
                "input": query,
                # "context": [],
                "chat_history": [],
            },
            config={'callbacks': [ConsoleCallbackHandler()]}
            # verbose=True
        )
        # pprint(out_dict)
        print(out_dict["answer"])

    def test_rag_with_llm_not_finished_yet(self):
        query = "What did the president say about Ketanji Brown Jackson?"

        # build a vector store from the state_of_the_union.txt file in the data folder
        vectorstore = get_file_vector_store()
        docs = vectorstore.similarity_search(query)

        # create prompt
        template = """You are a chatbot having a conversation with a human.

                Given the following extracted parts of a long document and a question, create a final answer.

                {context}

                {chat_history}
                Human: {human_input}"""

        prompt = PromptTemplate(input_variables=["chat_history", "human_input", "context"], template=template)

        # create chain
        chain = LLMChain(llm=get_llm(), prompt=prompt, verbose=True)

        out_dict = chain.invoke(
            {
                "human_input": query,
                # TODO: how to pass docs???
                "context": docs,
                "chat_history": [],
            },
            # config={'callbacks': [ConsoleCallbackHandler()]}
            verbose=True
        )
        print(out_dict)
        # print(out_dict["answer"])


if __name__ == '__main__':
    unittest.main()
