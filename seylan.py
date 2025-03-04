from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
from datetime import datetime
import time

def scrape_seylan_exchange_rates():
    # Set up Chrome options for headless mode
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver
    #service = Service(ChromeDriverManager().install())
    #driver = webdriver.Chrome(service=service, options=chrome_options)
    hub_url = "http://localhost:4444"
    driver = webdriver.Remote(command_executor=hub_url, options=options)

    try:
        # Navigate to the Seylan Bank exchange rates page
        driver.get("https://www.seylan.lk/exchange-rates")

        # Extract the last update date
        update_date_element = driver.find_element(By.XPATH, "/html/body/div[5]/div/div/h3/span")
        update_date_text = update_date_element.text.strip()
        #print(f"Update Date: {update_date_text}")

        # Find the table
        table = driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[2]/div/table")
        rows = table.find_elements(By.TAG_NAME, "tr")[2:]  # Skip header rows

        # Prepare data for CSV
        exchange_rates = []
        
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            
            # Skip rows without enough cells
            if len(cells) < 9:
                continue
            
            # Extract currency details
            currency_name = cells[0].text.split('\n')[-1].strip()
            currency_code = cells[1].text.strip()
            
            exchange_rates.append({
                'currency_name': currency_name,
                'currency_code': currency_code,
                'Currency Notes Buying': cells[2].text.strip(),
                'Currency Notes Selling': cells[3].text.strip(),
                'Traveller\'s Cheques/Drafts Buying': cells[4].text.strip(),
                'Traveller\'s Cheques/Drafts Selling': cells[5].text.strip(),
                'Telegraphic Transfers Buying': cells[6].text.strip(),
                'Telegraphic Transfers Selling': cells[7].text.strip(),
                'Import Bills Selling': cells[8].text.strip()
            })

        # Save to CSV
        if not exchange_rates:
            print("No exchange rates found!")
            return None

        csv_filename = f"exchange_rates_seylan.csv"
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['currency_name', 'currency_code', 
                          'Currency Notes Buying', 'Currency Notes Selling', 
                          'Traveller\'s Cheques/Drafts Buying', 'Traveller\'s Cheques/Drafts Selling', 
                          'Telegraphic Transfers Buying', 'Telegraphic Transfers Selling', 
                          'Import Bills Selling']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for rate in exchange_rates:
                writer.writerow({
                    **rate
                })
            csvfile.write(update_date_text)

        print(f"Seylan Data successfully saved to exchange_rates_seylan.csv")
        return csv_filename

    except Exception as e:
        print(f"A critical error occurred: {e}")
        return None

    finally:
        driver.quit()

scrape_seylan_exchange_rates()
