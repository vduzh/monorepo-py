from typing import Union, Sequence

import bs4
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader, WebBaseLoader
from langchain_community.vectorstores.chroma import Chroma

from libs.langchain.model import get_embeddings

# Load environment variables from .env file
load_dotenv()


def build_vector_store_from_text_file(path="state_of_the_union.txt", chunk_size=1000, chunk_overlap=0):
    # Load data from the file
    loader = TextLoader("./data/" + path)
    documents = loader.load()

    # Break large Documents into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(documents)

    # Store and index the splits
    return Chroma.from_documents(chunks, get_embeddings())


def build_vector_store_from_urls(
        web_paths: Union[str, Sequence[str]] = "https://lilianweng.github.io/posts/2023-06-23-agent/",
        chunk_size=1000,
        chunk_overlap=0):
    # Load data from the ut
    loader = WebBaseLoader(
        web_paths=web_paths,
        bs_kwargs=dict(parse_only=bs4.SoupStrainer(class_=("post-content", "post-title", "post-header"))))
    documents = loader.load()

    # Break large Documents into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(documents)

    # Store and index the splits
    return Chroma.from_documents(chunks, get_embeddings())
