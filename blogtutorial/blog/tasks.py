from celery import shared_task
import requests
from .models import NewsArticle

@shared_task
def fetch_news():
    response = requests.get('https://newsapi.org/v2/top-headlines', params={
        'country': 'us',
        'apiKey': 'YOUR_API_KEY'
    })
    news_data = response.json()

    for article in news_data.get('articles', []):
        NewsArticle.objects.update_or_create(
            title=article['title'],
            defaults={
                'content': article['description'],
                'published_date': article['publishedAt'],
                'source': article['source']['name']
            }
        )
