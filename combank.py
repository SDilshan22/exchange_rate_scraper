from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import time


# Step 1: Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run headless Chrome
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')  # Add user-agent
 
hub_url = "http://localhost:4444"
 
#driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver = webdriver.Remote(command_executor=hub_url, options=options)

# Initialize driver
url = 'https://www.combank.lk/rates-tariff#exchange-rates'

try:
    driver.get(url)
    
    # Wait for table to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.with-border'))
    )
    
    #time.sleep(5)
    
    # Extract last updated date
    date_text = driver.find_element(
        By.CSS_SELECTOR, 'th[colspan="6"] p').text
    last_updated = date_text.split('as at ')[-1].strip()
    
    # Extract headers
    headers = [
        'Currency',
        'Type',
        'Buying Rate',
        'Selling Rate'
        #'Last Updated'
    ]
    
    # Extract data
    data = []
    rows = driver.find_elements(By.CSS_SELECTOR, 'table.with-border tbody tr')
    
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        
        if len(cells) >= 7:
            currency = cells[0].text.strip()
            
            # Three rate types: Currency Notes, Cheques, TT
            rate_types = ['Currency Notes', 'Cheques', 'Telegraphic Transfers']
            
            for i in range(3):
                rate_type = rate_types[i]
                buying = cells[1 + (i*2)].text.strip()
                selling = cells[2 + (i*2)].text.strip()
                
                if buying == '-' and selling == '-':
                    continue  # Skip empty entries
                
                data.append({
                    'Currency': currency,
                    'Type': rate_type,
                    'Buying Rate': buying,
                    'Selling Rate': selling
                    #'Last Updated': last_updated
                })

    # Export to CSV
    with open('exchange_rates_combank.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        f.write(date_text)
    
    print("Combank Data successfully saved to exchange_rates_combank.csv")

finally:
    driver.quit()
