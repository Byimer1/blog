import requests
from django.core.management.base import BaseCommand
from blog.models import NewsArticle

class Command(BaseCommand):
    help = 'Fetch latest news articles from an API'

    def handle(self, *args, **kwargs):
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
        self.stdout.write(self.style.SUCCESS('Successfully fetched and updated news articles'))
