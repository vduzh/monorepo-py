from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Load environment variables from .env file
load_dotenv()


def main():
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=200,
        chunk_overlap=0
    )

    loader = TextLoader("./data/facts.txt")
    docs = loader.load_and_split(text_splitter)

    db = Chroma.from_documents(
        docs,
        embedding=OpenAIEmbeddings(),
        # TODO: update unit tests!!!
        persist_directory="./tmp/emb"
    )


if __name__ == "__main__":
    main()
