from src.news_scraper import NewsScraper
from robocorp.tasks import task

@task
def main():
    scraper = NewsScraper()
    scraper.main()