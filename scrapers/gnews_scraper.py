from gnews import GNews
import newspaper
from newspaper import Article
from newspaper import Config
import pandas as pd
import re
from html import unescape

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

topics = ["WORLD", "NATION", "BUSINESS", "TECHNOLOGY", "ENTERTAINMENT", "SPORTS", "SCIENCE", "HEALTH"]

google_news = GNews(language='en', period='14d', max_results=500000)

articles = []
for topic in topics:
    json_resp = google_news.get_news_by_topic(topic)
    for resp in json_resp:
        try:
            article = google_news.get_full_article(resp['url'])
        except:
            continue
        articles.append(article)
        print(len(articles), end = ', ')

news = []
for i in articles:
    if i is not None:
        if len(i.text) > 0:
            news.append(i.text)


def clean_text(text):
    # Remove HTML tags
    clean = re.sub(r'<.*?>', '', text)

    # Decode HTML entities
    clean = unescape(clean)

    # Replace URLs with a space
    clean = re.sub(r'http[s]?://\S+', '', clean)

    # Remove all non-alphanumeric characters (optional: keep periods and commas)
    clean = re.sub(r'[^a-zA-Z0-9\s.,]', '', clean)

    # Replace multiple spaces with a single space
    clean = re.sub(r'\s+', ' ', clean).strip()

    return clean


clean_articles = [clean_text(article) for article in news]
df = pd.DataFrame({
    'news': clean_articles
})

df.to_csv('gnews.csv', index=False)