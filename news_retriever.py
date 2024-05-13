from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings
from transformers import BartForConditionalGeneration, AutoTokenizer

EMBEDDINGS = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
FAISS_PATH = "faiss_index"
model_path = 'finetuned_model'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = BartForConditionalGeneration.from_pretrained(model_path)

def retrieve_news_from_fasiss(text):

    vectordb = FAISS.load_local(FAISS_PATH, EMBEDDINGS)
    retriever = vectordb.as_retriever(score_threshold=0.7)
    docs = retriever.get_relevant_documents(text)
    return docs

def get_relevant_news(text):

    top_news = retrieve_news_from_fasiss(text)
    multinews = ""
    for news in top_news:
        multinews = multinews+ news.page_content + ' ||| '

    return multinews

def generate_multinews_summary(news):

    inputs = tokenizer(news, return_tensors="pt", max_length=1024, truncation=True)

    summary_ids = model.generate(inputs["input_ids"], num_beams=4, max_length=256)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


multiple_news = get_relevant_news("Latest news on basketball")
print(generate_multinews_summary(multiple_news))
