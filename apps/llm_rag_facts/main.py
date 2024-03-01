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

    # TODO: update unit tests!!!
    results = db.similarity_search_with_score(
        "What is an interesting fat about the English language?",
        # TODO: update unit tests!!!
        # 4 is default
        k=2
    )
    for result in results:
        doc = result[0]
        score = result[1]
        print(score, doc.page_content, sep="\n", end="\n\n")

    results = db.similarity_search(
        "What is an interesting fat about the English language?",
        k=1
    )
    for result in results:
        print(result.page_content)


if __name__ == "__main__":
    main()
