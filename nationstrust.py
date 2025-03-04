from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
from datetime import datetime
import time

def scrape_nations_trust_exchange_rates():
    # Set up Chrome options for headless mode
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

    hub_url = "http://localhost:4444"

    # Initialize the WebDriver
    #service = Service(ChromeDriverManager().install())
    #driver = webdriver.Chrome(service=service, options=chrome_options)
    driver = webdriver.Remote(command_executor=hub_url, options=options)

    try:
        # Navigate to the Nations Trust Bank exchange rates page
        driver.get("https://www.nationstrust.com/foreign-exchange-rates")

        # Find the table
        table = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div/table")
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row

        # Prepare data for CSV
        exchange_rates = []
        
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            
            # Skip rows without enough cells
            if len(cells) < 5:
                continue
            
            exchange_rates.append({
                'Currency Code': cells[0].text.strip(),
                'Currency Name': cells[1].text.strip(),
                'DD Buying Rate': cells[2].text.strip(),
                'Mid Rates': cells[3].text.strip(),
                'DD Selling Rate': cells[4].text.strip()
            })

        # Save to CSV
        if not exchange_rates:
            print("No exchange rates found!")
            return None

        csv_filename = f"exchange_rates_nationstrust.csv"
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['Currency Code', 'Currency Name', 'DD Buying Rate', 'Mid Rates', 'DD Selling Rate']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for rate in exchange_rates:
                writer.writerow(rate)

        print("Nationstrust Data successfully saved to exchange_rates_nationstrust.csv")
        return csv_filename

    except Exception as e:
        print(f"A critical error occurred: {e}")
        return None

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_nations_trust_exchange_rates()
