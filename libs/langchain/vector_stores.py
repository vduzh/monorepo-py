from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma

from libs.langchain.model import get_embeddings

# Load environment variables from .env file
load_dotenv()


def get_file_vector_store(path="state_of_the_union.txt", chunk_size=1000, chunk_overlap=0):
    with open("./data/" + path) as f:
        text = f.read()

    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(text)

    return Chroma.from_texts(chunks, get_embeddings(), metadatas=[{"source": i} for i in range(len(chunks))]
                             )
