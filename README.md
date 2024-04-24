# News Site RPA Bot

## Overview
This project is an automated bot designed to gather news articles from a specific website and store the relevant information in an Excel file. It allows users to specify a search topic and a target month for retrieving articles.

## Features
- Automated web scraping to collect news articles from a target website.
- User-defined search topic and month for filtering articles.
- Extraction of article metadata including title, date, author, description, and picture link.
- Analysis functions to count occurrences of search phrases in the article descriptions and detect the presence of money-related information.


## Usage
1. Upon running the bot, you will be prompted to enter the search topic and target month.
2. The bot will then scrape the specified website for news articles matching the criteria.
3. Extracted article data will be stored in an Excel file named `News.xlsx` located in the `output` folder.

## Requirements
- Python 3.x
- robocorp-browser
- rpaframework
