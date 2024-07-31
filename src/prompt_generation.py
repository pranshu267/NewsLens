from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import os

from dotenv import load_dotenv

load_dotenv()

llm = GooglePalm(google_api_key=os.environ["GOOGLE_API_KEY"], temperature=0.1)
EMBEDDINGS = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
FAISS_PATH = "faiss_index"

def get_qa_chain():

    vectordb = FAISS.load_local(FAISS_PATH, EMBEDDINGS)
    retriever = vectordb.as_retriever()
    prompt_template = """Given the following context and a question, generate a prompt which will be passed to a Stable Diffusion model for generating an image which is relevant to the context.

    CONTEXT: {context}

    QUESTION: {question}"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(llm=llm,
                                        chain_type="stuff",
                                        retriever=retriever,
                                        input_key="query",
                                        chain_type_kwargs={"prompt": PROMPT})

    return chain
