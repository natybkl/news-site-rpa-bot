import os
import re
from datetime import datetime
import requests

class NewsArticle:
    def __init__(self, title, picture, author, date, news):
        self.title = title
        self.picture = picture
        self.author = author
        self.date = date
        self.news = news

    def contains_money(self):
        money_pattern = r'\$[\d,.]+|\d+\s?(dollars|USD)'
        match = re.search(money_pattern, self.news)
        
        return match is not None
    
    def count_occurrences_in_description(self, search_phrase):
        count = 0
        news = self.news.lower()
        for phrase in search_phrase.split():
            count += news.count(phrase.lower())

        return count
    
    def parse_and_format_date(self):
        date_obj = datetime.strptime(self.date, "%b %d, %Y")
        formatted_date = date_obj.strftime("%Y-%m-%d") 
        month = date_obj.month

        return formatted_date, month