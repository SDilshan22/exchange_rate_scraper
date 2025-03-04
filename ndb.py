from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from bs4 import BeautifulSoup  # Import BeautifulSoup


# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run headless Chrome
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')  # Add user-agent

hub_url = "http://localhost:4444"

#driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver = webdriver.Remote(command_executor=hub_url, options=options)

# Load the webpage
url = "https://www.ndbbank.com/rates/exchange-rates"
driver.get(url)

# Extract the content
html_content = driver.page_source

# You can now parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table with exchange rates
table = soup.find('table')

# Extract the "Last Updated On" date
last_updated = soup.find('span', text=lambda x: x and 'Last Updated On:' in x).text.strip().replace('Last Updated On: ', '')

# Extract data
data = []
for row in table.find_all('tr')[1:]:  # Skip the header row
    cols = row.find_all('td')
    if len(cols) > 0:
        currency_name = cols[0].find('ul').li.text.strip()
        currency_code = cols[1].find('ul').li.text.strip()
        buying_rate = cols[2].find('ul').li.text.strip()
        selling_rate = cols[3].find('ul').li.text.strip()
        demand_draft_buying_rate = cols[4].find('ul').li.text.strip()
        demand_draft_selling_rate = cols[5].find('ul').li.text.strip()
        telegraphic_transfer_buying_rate = cols[6].find('ul').li.text.strip()
        telegraphic_transfer_selling_rate = cols[7].find('ul').li.text.strip()
        
        data.append([currency_name, currency_code, buying_rate, selling_rate, 
                      demand_draft_buying_rate, demand_draft_selling_rate, 
                      telegraphic_transfer_buying_rate, telegraphic_transfer_selling_rate])

# Save to CSV
df = pd.DataFrame(data, columns=['Currency Name', 'Currency Code', 'Buying Rate', 
                                  'Selling Rate', 'Demand Draft Buying Rate', 
                                  'Demand Draft Selling Rate', 
                                  'Telegraphic Transfers Buying Rate', 
                                  'Telegraphic Transfers Selling Rate'])

# Add the last updated date as a new column
#df['Last Updated On'] = last_updated
#df.to_csv('ndb_exchange_rates.csv', index=False)

# Save the last updated info at the top of the CSV file
with open('exchange_rates_ndb.csv', 'w') as f:
    df.to_csv(f, index=False)  # Append the DataFrame below it
    f.write(f"Last Updated On: {last_updated}\n")  # Write the last updated info

print("NDB Data successfully saved to exchange_rates_ndb.csv")
# Close the driver
driver.quit()
