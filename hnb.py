from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import time


def clean_header(text):
    """Combine multi-line headers into single line"""
    return ' '.join(text.replace('\n', ' ').split()).strip()

def scrape_hnb_exchange_rates():
    # Configure browser
    options = Options()
    #options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    hub_url = "http://localhost:4444"

    # Initialize driver
    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Remote(command_executor=hub_url, options=options)
    
    try:
        driver.get("https://www.hnb.net/exchange-rates")
        
        # Wait for table to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table"))
        )
        #time.sleep(5)  # Additional buffer

        # Get updated date
        #updated_date = driver.find_element(By.XPATH, '//p[contains(text(), "Last updated:")]').text.split(":")[1].strip()
        updated_date = driver.find_element(By.XPATH, '//p[contains(text(), "Last updated:")]').text.strip()
        
        # Extract table data
        rates = []
        table = driver.find_element(By.CSS_SELECTOR, "table.table")
        header_row = table.find_element(By.CSS_SELECTOR, "tr:first-child")
        headers = [clean_header(h.text) for h in header_row.find_elements(By.CLASS_NAME, "exrateHead")]

        # Verify expected headers
        expected_headers = [
            "Currency",
            "Currency Code",
            "Telegraphic Transfer Buying Rate (LKR)",
            "Telegraphic Transfer Selling Rate (LKR)"
        ]

        if headers != expected_headers:
            print(f"Header mismatch detected. Expected {expected_headers}, got {headers}")
            return None
        
        # Extract data
        rates = []
        for row in table.find_elements(By.CSS_SELECTOR, "tr:not(:first-child)"):
            cells = row.find_elements(By.CLASS_NAME, "exrateText")
            
            if len(cells) != 4 or not cells[0].text:
                continue  # Skip empty/invalid rows
                
            rate_data = {
                headers[0]: cells[0].text.strip(),
                headers[1]: cells[1].text.strip(),
                headers[2]: cells[2].text.strip(),
                headers[3]: cells[3].text.strip()
            }
            rates.append(rate_data)

        #print(f"Successfully scraped {len(rates)} currency rates")
        #for row in table.find_elements(By.CSS_SELECTOR, "tbody tr"):
        #    cells = row.find_elements(By.TAG_NAME, "td")
        #    
        #    # Skip header and empty rows
        #    if len(cells) != 4 or not cells[0].text:
        #        continue
        #        
        #    currency = cells[0].text.strip()
        #    code = cells[1].text.strip()
        #    buying = cells[2].text.strip()
        #    selling = cells[3].text.strip()
        #    
        #    rates.append({
        #        "Currency": currency,
        #        "Code": code,
        #        "Buying Rate (LKR)": buying,
        #        "Selling Rate (LKR)": selling
        #        #"Last Updated": updated_date
        #    })
        # del rates[0]
        #print(f"Scraped {len(rates)} currencies")
        
        # Save to CSV
        with open('exchange_rates_hnb.csv', 'w', newline='', encoding='utf-8') as f:
            #writer = csv.DictWriter(f, fieldnames=["Currency", "Code", "Buying Rate (LKR)", "Selling Rate (LKR)"])
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rates)
            f.write(updated_date)
        print("HNB Data successfully saved to exchange_rates_hnb.csv") 
        return rates

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()

data = scrape_hnb_exchange_rates()
