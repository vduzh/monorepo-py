from typing import List

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore

from apps.llm_rag_facts.llm_utils import get_chat_model, get_embeddings

# set_debug(True)

# Load environment variables from .env file
load_dotenv()


class RedundantFilterRetriever(BaseRetriever):
    vector_store: VectorStore

    def _get_relevant_documents(
            self,
            query: str,
            *,
            run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        # calculate embedding fot the 'query' string
        emb = self.vector_store.embeddings.embed_query(query)

        # take embedding and feed them into that max_marginal_relevance_search_by_vector
        return self.vector_store.max_marginal_relevance_search_by_vector(emb)


def main():
    # initialize a vector store
    vector_store = Chroma(
        persist_directory="./tmp/emb",
        embedding_function=get_embeddings()
    )

    # create a retriever
    retriever = RedundantFilterRetriever(vector_store=vector_store)

    # build a chain
    chain = RetrievalQA.from_chain_type(
        llm=get_chat_model(),
        retriever=retriever,
        chain_type="stuff"
    )

    print("Sample:", "What is an interesting fact about the English language?")
    print("Use exit to leave the program")
    while True:
        query = input("\nUser: ")
        if query == "exit":
            break

        # invoke the chain
        out = chain.invoke({"query": query})
        # show the result
        print(out["result"])


if __name__ == "__main__":
    main()
