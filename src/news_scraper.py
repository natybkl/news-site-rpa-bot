import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from robocorp import browser
from robocorp.tasks import task
from RPA.Excel.Files import Files as Excel
from src.news_article import NewsArticle

class NewsScraper:
    def __init__(self):
        load_dotenv()

    def main(self):
        search_query = os.getenv("SEARCH_QUERY")
        news_timeframe = int(os.getenv("NEWS_TIMEFRAME"))
        category = os.getenv("CATEGORY")

        self.scrape_news(search_query, news_timeframe, category)

    def scrape_news(self, search_query, news_timeframe, category):
        browser.configure(
            browser_engine="chromium",
            screenshot="only-on-failure",
            headless=False,
        )
        try:
            page = browser.goto("https://gothamist.com/")

            search_button = page.locator("css=.search-button button")
            search_button.click()

            search_input = page.locator("css=input.search-page-input")
            search_input.fill(search_query)

            search_button = page.locator("css=button.search-page-button")
            search_button.click()

            # Wait for the search results to load
            page.wait_for_selector("css=.search-page-results")

            while True:
                load_button = page.locator("css=button.p-button.p-component.p-button-rounded[aria-label='Load More']")
                try:
                    load_button.click()
                except Exception as e:
                    break

            title_divs = page.query_selector_all("css=div.v-card")

            excel_file = Excel()
            output_folder = Path(__file__).resolve().parent.parent / "data" / "News.xlsx"
            excel_file.open_workbook(output_folder)

            if "News" not in excel_file.list_worksheets():
                headers = {
                    "Title": [],
                    "Date": [],
                    "Author": [],
                    "Description": [],
                    "Search Phrase Count": [],
                    "Contains Money": [],
                    "Picture Link": []
                }
                
                excel_file.create_worksheet("News", headers, exist_ok=True, header=True)

            news_links = ["https://gothamist.com" + div.query_selector("css=a").get_attribute('href') for div in title_divs]

            for news_link in news_links[:10]:
                title, picture, author, date, news = self.get_news_details(news_link)
        
                news_article = NewsArticle(title, picture, author, date, news)

                formatted_date, month = news_article.format_date()
                search_phrase_count = news_article.count_search_phrases(search_query)
                news_contains_money = news_article.contains_money()

                current_month = datetime.now().month

                if month + news_timeframe < current_month:
                    break

                data = {
                    "Title": [title],
                    "Date": [formatted_date],
                    "Author": [author],
                    "Description": [news],
                    "Search Phrase Count": [search_phrase_count],
                    "Contains Money": [news_contains_money],
                    "Picture Link": [picture]
                }
                
                excel_file.append_rows_to_worksheet(content=data, name="News", header=True)
                page.wait_for_timeout(100)

            excel_file.save_workbook()
            excel_file.close_workbook()
            

        except Exception as e:
            print(f"An error occurred: {e}")

    def get_news_details(self, news_link):
        new_page = browser.goto(news_link)

        new_page.wait_for_selector("css=div.content")

        title = new_page.query_selector("css=h1").inner_text()
        picture = new_page.query_selector("css=.image-with-caption-image img").get_attribute('src')
        author = new_page.query_selector("css=a.v-byline-author-name").inner_text()
        raw_date = new_page.query_selector("css=.date-published p.type-caption").inner_text()
        date = ' '.join(raw_date.split()[1:])
        paragraphs = new_page.query_selector_all("css=.streamfield.article-body .streamfield-paragraph.rte-text p")

        news_content = ""
        for paragraph in paragraphs:
            news_content = news_content + paragraph.inner_text() + '\n' + '\n'

        return title, picture, author, date, news_content
