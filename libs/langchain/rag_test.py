import unittest
from pprint import pprint

from langchain import hub
from langchain.chains import create_retrieval_chain, LLMChain, RetrievalQA
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.tracers import ConsoleCallbackHandler

from libs.langchain.model import get_llm, get_chat_model
from libs.langchain.vector_stores import build_vector_store_from_text_file, build_vector_store_from_urls


# https://python.langchain.com/docs/use_cases/question_answering/
class TestRetrievalAugmentedGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # build a vector store from the state_of_the_union.txt file in the data folder
        # cls.vectorstore = build_vector_store_from_text_file()
        pass

    def test_rag_with_retrieval_chain(self):
        # create a vector store
        vectorstore = build_vector_store_from_text_file()
        vector_store_retriever = vectorstore.as_retriever()

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

        # cleanup
        vectorstore.delete_collection()

    # def format_docs(self, docs):
    #     return "\n\n".join(doc.page_content for doc in docs)

    def test_qa_with_retrieval_qa(self):
        # create a vector store from https://lilianweng.github.io/posts/2023-06-23-agent/
        vectorstore = build_vector_store_from_urls()
        retriever = vectorstore.as_retriever()

        # Create a prompt
        prompt = hub.pull("rlm/rag-prompt")
        prompt_text = prompt.invoke({'context': "Some context", "question": "Some question"})
        print("prompt_text:\n", "\n".join(m.content for m in prompt_text.to_messages()))

        # Build a chain
        # qa_runnable = (
        #         {
        #             # "context": retriever | self.format_docs,
        #             "context": retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)),
        #             "question": RunnablePassthrough()
        #         }
        #         | prompt
        #         | get_chat_model()
        #         | StrOutputParser()
        # )
        qa_chain = RetrievalQA.from_chain_type(
            get_chat_model(),
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt}
        )

        # Invoke the chain
        question = "What are the approaches to Task Decomposition?"
        # result = qa_runnable.invoke(question)
        result = qa_chain(question)
        pprint(result)

        # cleanup
        vectorstore.delete_collection()

    def test_rag_with_llm_not_finished_yet(self):
        query = "What did the president say about Ketanji Brown Jackson?"

        # build a vector store from the state_of_the_union.txt file in the data folder
        vectorstore = build_vector_store_from_text_file()
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
