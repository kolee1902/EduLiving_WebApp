from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import math
import re
sys.stdout.reconfigure(encoding='utf-8')


# Update path to msedgedriver
edge_driver_path = "D:/edgedriver_win64/msedgedriver.exe" 

# Configure Microsoft Edge browser
edge_options = Options()
edge_options.add_argument('--headless')

# Initialize WebDriver for Edge
service = Service(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service, options=edge_options)

with open('Type.txt', 'r') as file:
    types = [line.strip() for line in file.readlines()]

for type in types:
    filename = re.sub(r'[\\/*?:"<>|]', "", type)
    file = open(f"{filename}.txt", "w") 
    driver.get(f"{type}{1}")
    pages_str = driver.find_elements(By.TAG_NAME, "b")[1].text
    pages = int(pages_str.replace(".", ""))
    pages = math.ceil(pages / 15)
    
    for page in range(1, pages+1):
        driver.get(f"{type}{page}")
        elements = driver.find_elements(By.CSS_SELECTOR, ".prop-info")
        for element in elements:
            file.write(element.find_element(By.CLASS_NAME, "link-overlay").get_attribute("href"))
            file.write("\n")
        print(page)

    file.close()