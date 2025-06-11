import requests
from bs4 import BeautifulSoup

class Aggregator:
    def __init__(self):
        self.tinkoff_blog_url = "https://www.tinkoff.ru/blog/"
        self.news_api_key = "52a71ffd7a3b437681015a5199aef88f"

    def scrape_tinkoff_blog(self):
        response = requests.get(self.tinkoff_blog_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = []
        for item in soup.select('.post-card'):  # Adjust CSS selector as needed
            title = item.find('h2').get_text(strip=True)
            link = item.find('a')['href']
            articles.append({'title': title, 'link': link})

        return articles

    def fetch_financial_news(self):
        url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={self.news_api_key}"
        response = requests.get(url).json()

        articles = []
        for article in response['articles']:
            title = article['title']
            description = article['description']
            link = article['url']
            articles.append({'title': title, 'description': description, 'link': link})

        return articles

    def get_updates(self):
        tinkoff_articles = self.scrape_tinkoff_blog()
        financial_news = self.fetch_financial_news()

        updates = {
            "tinkoff_blog": tinkoff_articles[:3],  # Top 3 Tinkoff blog posts
            "financial_news": financial_news[:3]   # Top 3 financial news articles
        }
        return updates