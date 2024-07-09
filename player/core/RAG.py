from langchain.vectorstores import chroma
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai.llms import GoogleGenerativeAI
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.document_loaders import pdf, text
from langchain.schema.document import Document


palm_api_key="AIzaSyBZ00vqmEJufpuT0V7vOVBm0ESAjpBUcow"
def answer_query(dir,question:str) -> str:

    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = chroma.Chroma(persist_directory=dir, embedding_function=embedding_function)
    
    llm = GoogleGenerativeAI(model="gemini-pro",google_api_key=palm_api_key)
    template = """Know are the best teacher in the world.Use the following pieces of context to answer the question at the end. If you don't know the answer, 
    just say that you don't know, don't try to make up an answer. Be clear so your students well . Always say "thanks for asking!" at the end of the answer. 
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    retriever= vectordb.as_retriever()
    qa = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        memory=memory
    )

    result = qa({"question": question})

    return result['answer']

