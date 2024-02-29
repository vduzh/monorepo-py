import unittest
from operator import itemgetter

from langchain import hub
from langchain.chains import LLMChain, create_retrieval_chain, SequentialChain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
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

        out_dict = chain.invoke({"product": "colorful socks"})
        # pprint(out_dict)

        # contains all the inputs
        self.assertEqual("colorful socks", out_dict["product"])
        # contains the generated result
        self.assertIsNotNone(out_dict["text"])

    def test_create_chain_with_output_key(self):
        chain = LLMChain(
            llm=self._llm,
            prompt=PromptTemplate.from_template("What is a good name for a company that makes {product}?"),
            output_key="company_name"
        )

        out_dict = chain.invoke({"product": "colorful socks"})
        # contains the generated result under the company_name key
        self.assertIsNotNone(out_dict["company_name"])

    def test_create_chain_with_lcel(self):
        prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
        chain = prompt | self._llm

        out_str = chain.invoke({"product": "colorful socks"})

        self.assertIsInstance(out_str, str)

    def test_reuse_chain_with_sequential_chain(self):
        code_chain = LLMChain(
            llm=self._llm,
            prompt=PromptTemplate.from_template("Write a {language} function that will {task}."),
            output_key="code"
        )

        test_chain = LLMChain(
            llm=self._llm,
            prompt=PromptTemplate.from_template("Write a unit-test for the following {language} code: {code}"),
            output_key="test"
        )

        chain = SequentialChain(
            chains=[code_chain, test_chain],
            input_variables=["language", "task"],
            output_variables=["code", "test"],
        )

        out = chain.invoke({"language": "python", "task": "return a list of numbers"})
        print(">>>>>>>> GENERATED Python CODE:", out["code"])
        print(">>>>>>>> GENERATED Python TEST:", out["test"])

    # https://python.langchain.com/docs/expression_language/cookbook/multiple_chains
    def test_reuse_chain_with_sequential_lcel(self):
        prompt = PromptTemplate.from_template("Write a {language} function that will {task}.")
        reused_chain = prompt | self._llm

        prompt_1 = PromptTemplate.from_template("Write a unit-test for the following {language} code: {code}")
        chain_1 = prompt_1 | self._llm

        # chain = reused_chain | RunnableLambda(lambda txt: {"product": txt}) | chain_1
        chain = (
                {
                    "code": reused_chain,
                    "language": itemgetter("language")
                }
                | RunnableLambda(lambda data: data)
                | {
                    "code": itemgetter("code"),
                    "test": chain_1
                }
        )
        out_dict = chain.invoke({"language": "Java", "task": "return a list of numbers"})

        print(">>>>>>>> GENERATED Java CODE:", out_dict["code"])
        print(">>>>>>>> GENERATED Java TEST:", out_dict["test"])

    def test_create_stuff_documents_chain_lcel_chain(self):
        prompt = ChatPromptTemplate.from_messages(
            [("system", "What are everyone's favorite colors:\n\n{context}")]
        )
        chain = create_stuff_documents_chain(self._llm, prompt)

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

    # def test_chain(self):
    #     prompt_template = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
    #     runnable = {"product": lambda x: x["input"]} | prompt_template
    #     print("test_chain:", runnable)
    #     out = runnable.invoke({"input": "colorful socks"})
    #     print("test_chain:", out)
    #
    # def test_basic_chain(self):
    #     prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
    #     # chain = prompt | self._llm | self._output_parser
    #     # out = chain.invoke({"product": "colorful socks"})
    #


if __name__ == '__main__':
    unittest.main()
