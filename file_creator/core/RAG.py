from typing import List
from langchain.vectorstores import chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.document_loaders import pdf
from langchain.schema.document import Document


def create_vector_db(text:str, files:list) -> chroma.Chroma:


    documents= []
    transcript:List[Document] =  [Document(text)]
    documents.extend(transcript)
    if (len(files) > 0):
        for i in files:
            loader = pdf.PyPDFLoader(i)
            documents.extend(loader.load())
    

    # split it into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # create the open-source embedding function
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # load it into Chroma
    db = chroma.Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db")

    return db

