from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import math
import pandas as pd
import re
sys.stdout.reconfigure(encoding='utf-8')
from selenium.common.exceptions import NoSuchElementException


# Update path to msedgedriver
edge_driver_path = "D:/edgedriver_win64/msedgedriver.exe" 

# Configure Microsoft Edge browser
edge_options = Options()
edge_options.add_argument('--headless') 

# Initialize WebDriver for Edge
service = Service(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service, options=edge_options)

with open('final.txt', 'r') as file:
    links = [line.strip() for line in file.readlines()]

excel_file = 'data.xlsx'
df = pd.read_excel(excel_file)
j = 1

for link in links:
    driver.get(link)

    # Wait for the title to load (adjust the selector based on the actual page)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".title")))
    except TimeoutException:
        print(f"Timeout when trying to load the page: {link}. Skipping...")
        continue

    key_value = {}

    try:
        key_value["Tiêu đề"] = driver.find_element(By.CSS_SELECTOR, ".title").text
        key_value["Địa chỉ"] = driver.find_element(By.CSS_SELECTOR, ".address").text
        key_value["Giá"] = driver.find_element(By.CSS_SELECTOR, ".price").text
        key_value["Giới thiệu"] = driver.find_element(By.CSS_SELECTOR, ".info-content-body").text
        key_value["Loại BĐS"] = "Nhà hẻm ngõ"

        # Extract attributes from .info-attrs
        element = driver.find_element(By.CSS_SELECTOR, ".info-attrs.clearfix")
        lines = element.text.strip().split('\n')
        for i in range(0, len(lines), 2): 
            key = lines[i].strip()
            value = lines[i + 1].strip()
            key_value[key] = value

        # Try to extract additional details from .list-unstyled
        try:
            element = driver.find_element(By.CSS_SELECTOR, ".list-unstyled.clearfix")
            lines = element.text.strip().split('\n')
            for i in range(0, len(lines), 2):
                key = lines[i].strip()
                value = lines[i + 1].strip()
                key_value[key] = value
        except NoSuchElementException:
            pass  

    except NoSuchElementException:
        print(f"Could not extract information from {link}. Skipping...")
        continue

    new_row = pd.DataFrame([key_value])
    df = pd.concat([df, new_row], ignore_index=True)

    # Periodically save to avoid data loss in case of failure
    if j % 10 == 0:
        df.to_excel('data.xlsx', index=False)
        print(f"Saved data after processing {j} links.")

    print(f"Processed link {j}")
    j += 1

# Save the final DataFrame to Excel
df.to_excel('data.xlsx', index=False)
print("Scraping complete. Data saved to 'data.xlsx'.")

driver.quit()