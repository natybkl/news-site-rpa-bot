# News Site RPA Bot

## Overview
This project is an automated bot designed to gather news articles from a specific website and store the relevant information in an Excel file. It allows users to specify a search topic and a target month for retrieving articles.

## Features
- Automated web scraping to collect news articles from a target website.
- User-defined search topic and month for filtering articles.
- Extraction of article metadata including title, date, author, description, and picture link.
- Analysis functions to count occurrences of search phrases in the article descriptions and detect the presence of money-related information.

## File Hierarchy
- `.env`: Configuration file for environment variables.
- `.gitignore`: File specifying which files and directories to ignore in Git.
- `README.md`: Project documentation.
- `robot.yaml`: Robocorp project configuration file.
- `tasks.py`: Main Python script containing task definitions.
- `conda.yaml`: Conda environment configuration file.
- `data/`: Directory for data files.
  - `News.xlsx`: Excel file for storing news data.
  - `input.json`: JSON file containing input variables.
- `src/`: Source code directory.
  - `__init__.py`: Python package initializer.
  - `news_article.py`: Module for NewsArticle class.
  - `news_scraper.py`: Main module for NewsScraper class.

## Usage
1. Ensure all dependencies are installed and configured.
2. Update the `input.json` file located in the `data` folder with the desired search topic, news timeframe, and category.
3. Run the `tasks.py` script to initiate the bot.
4. Extracted article data will be stored in the `News.xlsx` Excel file located in the `data` folder.

## Requirements
- Python 3.x
- robocorp-browser
- rpaframework
