from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

def scrape_exchange_rates():
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run headless Chrome
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')  # Add user-agent

    hub_url = "http://localhost:4444"

    # Initialize Chrome WebDriver
    #driver = webdriver.Chrome()
    driver = webdriver.Remote(command_executor=hub_url, options=options)
    driver.get("https://www.sampath.lk/rates-and-charges?activeTab=exchange-rates")

    try: 
        # Scroll down a bit to trigger lazy loading of the table
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(5)  # Pause to allow the new content to load
        
        # Directly locate the exchange rates table by its XPath
        #table = driver.find_element(By.XPATH, '//*[@id="__BVID__399"]')
        table = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[2]/div/div[2]/div/div/div[2]/div[3]/section[1]/div/div[2]/div/div/div[2]/div/table')
        timestamp = driver.find_element(By.XPATH, '//*[@id="__BVID__336"]/section[1]/div/div[2]/div/div/div[1]/p').text
        
        # Extract table headers
        headers = [th.text.strip() for th in table.find_elements(By.XPATH, './/thead//th')]

        # Extract table data
        data = []
        for row in table.find_elements(By.XPATH, './/tbody/tr'):
            cols = row.find_elements(By.TAG_NAME, 'td')
            data.append([col.text.strip() for col in cols])

        # Write the data to a CSV file
        with open('exchange_rates_sampath.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)  # Write headers
            writer.writerows(data)     # Write data rows
            writer.writerow([])        # Empty row for separation
            f.write(timestamp)

    finally:
        print("Sampath Data successfully saved to exchange_rates_sampath.csv")
        driver.quit()

scrape_exchange_rates()
