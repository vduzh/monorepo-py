import unittest
from pprint import pprint

from langchain import hub
from langchain.chains import LLMChain, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.vectorstores.docarray import DocArrayInMemorySearch
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.tracers import ConsoleCallbackHandler

from model import get_llm, get_embeddings


def get_documents_from_file(name: str = "state_of_the_union.txt"):
    return CharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(
        TextLoader("./data/" + name).load()
    )


class TestChain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._llm = get_llm()
        cls._output_parser = StrOutputParser()

    @classmethod
    def tearDownClass(cls):
        cls._llm = None

    def test_create_chain(self):
        prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
        chain = LLMChain(llm=self._llm, prompt=prompt)
        pprint(chain)

        # execute chain
        # res = chain.run(product="colorful socks")

    def test_create_chain_with_lcel(self):
        prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
        chain = prompt | self._llm | self._output_parser
        print(chain)

        # out = chain.invoke({"product": "colorful socks"})

    def test_create_stuff_documents_chain_lcel_chain(self):
        prompt = ChatPromptTemplate.from_messages(
            [("system", "What are everyone's favorite colors:\n\n{context}")]
        )
        llm = get_llm()
        chain = create_stuff_documents_chain(llm, prompt)

        docs = [
            Document(page_content="Jesse loves red but not yellow"),
            Document(page_content="Jamal loves green but not as much as he loves orange")
        ]
        out_text = chain.invoke({"context": docs}, config={'callbacks': [ConsoleCallbackHandler()]})
        print(out_text)

    def test_create_retrieval_chain_lcel_chain(self):
        vectorstore = Chroma.from_documents(
            get_documents_from_file("state_of_the_union.txt"),
            get_embeddings()
        )
        retriever = vectorstore.as_retriever()

        prompt = hub.pull("langchain-ai/retrieval-qa-chat")

        combine_docs_chain = create_stuff_documents_chain(get_llm(), prompt)

        retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

        out_dict = retrieval_chain.invoke(
            {
                "input": "What did the president say about Ketanji Brown Jackson?",
                "context": [],
                "chat_history": [],
            },
            # config={'callbacks': [ConsoleCallbackHandler()]}
        )
        # pprint(out_dict)
        print(out_dict["answer"])

    # def test_basic_chain(self):
    #     prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
    #     chain = prompt | self._llm | self._output_parser
    #     # out = chain.invoke({"product": "colorful socks"})

    # def test_basic_chain(self):
    #     chat_prompt_template = ChatPromptTemplate.from_messages([
    #         ("system", "You are world class technical documentation writer."),
    #         ("user", "{input}")
    #     ])
    #
    #     # LangChain Expression Language (LCEL)
    #     chain = chat_prompt_template | self._llm | self._output_parser
    #
    #     out = chain.invoke({"input": "how can langsmith help with testing?"})    #


if __name__ == '__main__':
    unittest.main()
