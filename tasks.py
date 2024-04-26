# import os
# import re
# from datetime import datetime
# from pathlib import Path
# from dotenv import load_dotenv
# import requests
# from robocorp import browser
# from robocorp.tasks import task
# from RPA.Robocorp.WorkItems import WorkItems
# from RPA.Excel.Files import Files as Excel


# @task
# def main():
#     load_dotenv()

#     search_query = os.getenv("SEARCH_QUERY")
#     news_timeframe = int(os.getenv("NEWS_TIMEFRAME"))
#     category = os.getenv("CATEGORY")

#     scrape_news(search_query, news_timeframe, category)


# def scrape_news(search_query, news_timeframe, category):
#     browser.configure(
#         browser_engine="chromium",
#         screenshot="only-on-failure",
#         headless=False,
#     )
#     try:
#         page = browser.goto("https://gothamist.com/")

#         search_bar_button = page.locator("css=.search-button button")
#         search_bar_button.click()

#         search_bar_input = page.locator("css=input.search-page-input")
#         search_bar_input.fill(search_query)

#         search_button = page.locator("css=button.search-page-button")
#         search_button.click()

#         # Wait for the search results to load
#         page.wait_for_selector("css=.search-page-results")

#         while True:
#             load_button = page.locator("css=button.p-button.p-component.p-button-rounded[aria-label='Load More']")
#             try:
#                 load_button.click()
#             except Exception as e:
#                 break

#         title_divs = page.query_selector_all("css=div.v-card")

#         excel_file = Excel()
#         output_folder = Path(__file__).resolve().parent / "data" / "News.xlsx"
#         excel_file.open_workbook(output_folder)

#         if "News" not in excel_file.list_worksheets():
#             headers = {
#                 "Title": [],
#                 "Date": [],
#                 "Author": [],
#                 "Description": [],
#                 "Search Phrase Count": [],
#                 "Contains Money": [],
#                 "Picture Link": []
#             }
            
#             excel_file.create_worksheet("News", headers, exist_ok=True, header=True)

#         news_links = ["https://gothamist.com" + div.query_selector("css=a").get_attribute('href') for div in title_divs]

#         for news_link in news_links[:10]:
#             title, picture, author, date, news = get_description(news_link)

#             formatted_date, month = parse_and_format_date(date)
#             search_phrase_count = count_occurrences_in_description(news, search_query)
#             news_contains_money = contains_money(news)

#             current_month = datetime.now().month

#             if month + news_timeframe < current_month:
#                 break

#             data = {
#                 "Title": [title],
#                 "Date": [formatted_date],
#                 "Author": [author],
#                 "Description": [news],
#                 "Search Phrase Count": [search_phrase_count],
#                 "Contains Money": [news_contains_money],
#                 "Picture Link": [picture]
#             }
            
#             excel_file.append_rows_to_worksheet(content=data, name="News", header=True)
#             page.wait_for_timeout(100)

#         excel_file.save_workbook()
#         excel_file.close_workbook()
        

#     except Exception as e:
#         print(f"An error occurred: {e}")


# def get_description(news_link):
#     new_page = browser.goto(news_link)

#     new_page.wait_for_selector("css=div.content")

#     title = new_page.query_selector("css=h1").inner_text()
#     picture = new_page.query_selector("css=.image-with-caption-image img").get_attribute('src')
#     author = new_page.query_selector("css=a.v-byline-author-name").inner_text()
#     raw_date = new_page.query_selector("css=.date-published p.type-caption").inner_text()
#     date = ' '.join(raw_date.split()[1:])
#     paragraphs = new_page.query_selector_all("css=.streamfield.article-body .streamfield-paragraph.rte-text p")

#     news = ""
#     for paragraph in paragraphs:
#         news = news + paragraph.inner_text() + '\n' + '\n'

#     return title, picture, author, date, news


# def parse_and_format_date(date_str):
#     date_obj = datetime.strptime(date_str, "%b %d, %Y")
#     formatted_date = date_obj.strftime("%Y-%m-%d") 
#     month = date_obj.month

#     return formatted_date, month


# def count_occurrences_in_description(news, search_phrases):
#     count = 0
#     for phrase in search_phrases.split():
#         count += news.lower().count(phrase.lower())

#     return count


# def contains_money(text):
#     money_pattern = r'\$[\d,.]+|\d+\s?(dollars|USD)'
#     match = re.search(money_pattern, text)
    
#     return match is not None


from src.news_scraper import NewsScraper
from robocorp.tasks import task

@task
def main():
    scraper = NewsScraper()
    scraper.main()