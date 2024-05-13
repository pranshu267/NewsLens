from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS

FAISS_PATH = "faiss_index"
EMBEDDINGS = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")

def load_documents():

    loader = CSVLoader(file_path="news.csv", source_column="news")

    documents = loader.load()
    return documents

def split_text(documents: list[Document]):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(documents)

    return chunks

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_faiss(chunks)

def save_to_faiss(chunks: list[Document]):

    vectordb = FAISS.from_documents(chunks, EMBEDDINGS)
    vectordb.save_local(FAISS_PATH)

if __name__ == "__main__":
    generate_data_store()