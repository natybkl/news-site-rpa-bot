from robocorp import browser
from robocorp.tasks import task
from datetime import datetime
from RPA.Excel.Files import Files as Excel

from pathlib import Path
import os
import re
import requests


@task
def search_us_election():
    browser.configure(
        browser_engine="chromium",
        screenshot="only-on-failure",
        headless=False,
    )
    try:
        page = browser.goto("https://gothamist.com/")

        # Click the search bar button to bring up the search input field
        search_bar_button = page.locator("css=.search-button button")
        search_bar_button.click()

        # Fill the search input field and press the search button
        search_bar_input = page.locator("css=input.search-page-input")
        search_bar_input.fill("US Election")
        search_button = page.locator("css=button.search-page-button")
        search_button.click()

        # Wait for the search results to load
        page.wait_for_selector("css=.search-page-results")

        # Wait for the search results to load
        page.wait_for_timeout(10000)
        
        title_divs = page.query_selector_all("css=div.v-card")

        # Initialize Excel file
        excel_file = Excel()
        output_folder = Path(__file__).resolve().parent / "output" / "News.xlsx"
        excel_file.open_workbook(output_folder)

        # headers = [["Title"], ["Date"], ["Author"], ["Description"], ["Picture Link"]]
        headers = {"Title":[], "Date":[], "Author":[], "Description":[], "Search Phrase Count":[], "Contains Money":[], "Picture Link":[]}

        excel_file.remove_worksheet("News")
        
        excel_file.create_worksheet("News", headers, exist_ok=True, header=True)
        
        
        # if not os.path.exists(output_folder):
        #     excel_file.create_workbook(output_folder)
        #     excel_file.create_worksheet("News", headers)
        # else:
        #     excel_file.open_workbook(output_folder)
        #     excel_file.create_worksheet("News", headers, overwrite=True)

        news_links = ["https://gothamist.com" + div.query_selector("css=a").get_attribute('href') for div in title_divs]

        for news_link in news_links[:5]:
            title, picture, author, date, news = get_description(news_link)

            formatted_date, month = parse_and_format_date(date)
            search_phrase_count = count_occurrences_in_description(news, "US Election")
            news_contains_money = contains_money(news)

             # Get the current month
            current_month = datetime.now().month

            # Compare the month with the current month
            if month < current_month:
                break

            data = {"Title":[title],
                    "Date": [formatted_date],
                    "Author": [author],
                    "Description": [news],
                    "Search Phrase Count":[search_phrase_count],
                    "Contains Money":[news_contains_money],
                    "Picture Link": [picture]}
            
            excel_file.append_rows_to_worksheet(content=data, name="News", header=True)
        #     print("Title:", title)
        #     print("Picture Link:", picture)
        #     print("News Link:", news_link)
        #     print("Author:", author)
        #     print("Date:", date)
        #     print("News:", len(news))
        #     print("--------------------")
        excel_file.save_workbook()
        excel_file.close_workbook()
        

    except Exception as e:
        print(f"An error occurred: {e}")

def get_description(news_link):
    new_page = browser.goto(news_link)

    new_page.wait_for_selector("css=div.content")

    title = new_page.query_selector("css=h1").inner_text()
    picture = new_page.query_selector("css=.image-with-caption-image img").get_attribute('src')
    author = new_page.query_selector("css=a.v-byline-author-name").inner_text()
    raw_date = new_page.query_selector("css=.date-published p.type-caption").inner_text()
    date = ' '.join(raw_date.split()[1:])
    paragrpahs = new_page.query_selector_all("css=.streamfield.article-body .streamfield-paragraph.rte-text p")

    news = ""
    for paragrpah in paragrpahs:
        news = news + paragrpah.inner_text() + '\n' + '\n'

    return title, picture, author, date, news


# Function to parse and format date string
def parse_and_format_date(date_str):
    date_obj = datetime.strptime(date_str, "%b %d, %Y")
    
    # Change the format as needed
    formatted_date = date_obj.strftime("%Y-%m-%d") 

    month = date_obj.month

    return formatted_date, month


def count_occurrences_in_description(news, search_phrases):
    count = 0
    for phrase in search_phrases.split():
        count += news.lower().count(phrase.lower())
        print(f"{phrase} count: {count}")
    return count

def contains_money(text):
    # Regular expression to match money formats
    money_pattern = r'\$[\d,.]+|\d+\s?(dollars|USD)'
    
    # Search for money pattern in the text
    match = re.search(money_pattern, text)
    
    # Return True if money pattern is found, False otherwise
    return match is not None