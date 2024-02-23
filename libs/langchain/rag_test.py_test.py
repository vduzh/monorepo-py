import unittest

from langchain_community.vectorstores.docarray import DocArrayInMemorySearch
from langchain_openai import OpenAIEmbeddings


class TestRetrievalAugmentedGeneration(unittest.TestCase):

    def test_(self):
        # https://python.langchain.com/docs/use_cases/question_answering/

        # vectorstore = Chroma.from_documents(
        #     get_documents_from_file("state_of_the_union.txt"),
        #     get_embeddings()
        # )
        # retriever = vectorstore.as_retriever()
        #
        # prompt = hub.pull("langchain-ai/retrieval-qa-chat")
        #
        # combine_docs_chain = create_stuff_documents_chain(get_llm(), prompt)
        #
        # retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
        #
        # out_dict = retrieval_chain.invoke(
        #     {
        #         "input": "What did the president say about Ketanji Brown Jackson?",
        #         "context": [],
        #         "chat_history": [],
        #     },
        #     # config={'callbacks': [ConsoleCallbackHandler()]}
        # )
        # # pprint(out_dict)
        # print(out_dict["answer"])
        pass


if __name__ == '__main__':
    unittest.main()
