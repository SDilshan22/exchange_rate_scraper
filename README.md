Exchange Rate Scraper 🌐💱
Overview

This project is a simple web scraping solution designed to extract exchange rates from multiple Sri Lankan banks. It utilizes Selenium WebDriver for web automation and supports scraping rates from various financial institutions.
Features

Web scraping for exchange rates
Supported banks:

        Commercial Bank
        Sampath Bank
        Nations Trust Bank
        HNB Bank
        Seylan Bank

Prerequisites

    Python: 3.12
    Docker: (optional, but recommended)

Dependencies

    selenium
    pandas
    beautifulsoup4
    webdriver-manager

Installation
Local Setup

    Clone the repository
    Install dependencies:
      pip install -r requirements.txt

Docker Setup

    Pull Selenium Chrome WebDriver
      docker run -d -e SE_NODE_MAX_SESSIONS=5 -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome:latest

    Build the Exchange Rate Scraper image and run container
      docker build -t exchange-rate-scraper .
      docker run -dit --name scraper --network=host exchange-rate-scraper

Project Structure

    combank.py: Commercial Bank scraper
    hnb.py: HNB Bank scraper
    nationstrust.py: Nations Trust Bank scraper
    sampath.py: Sampath Bank scraper
    seylan.py: Seylan Bank scraper
    ndb.py: NDB Bank scraper
    combine.py: Combines scraped data into one xlsx (excel book)
    executor.sh: Shell script for execution
    Dockerfile: Docker configuration

Usage

Run individual bank scrapers or use the combination script to collect exchange rates.

Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss proposed changes.
License

MIT
