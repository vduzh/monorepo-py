from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.chroma import Chroma

from projects.llm_rag_facts.llm_utils import get_embeddings


def main():
    # configure splitter
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=200,
        chunk_overlap=0
    )

    # create text loader
    loader = TextLoader("./data/facts.txt")

    # load documents
    docs = loader.load_and_split(text_splitter)

    # create a vectorstore from the list of documents
    Chroma.from_documents(
        docs,
        embedding=get_embeddings(),
        # TODO: update unit tests!!!
        persist_directory="./tmp/emb"
    )


if __name__ == "__main__":
    main()
