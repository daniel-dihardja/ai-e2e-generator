import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(override=True)

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Specify the path to the custom Chrome binary installed by Chrome for Testing
    chrome_path = os.getenv('CHROME_PATH')
    if chrome_path:
        options.binary_location = chrome_path

    # Specify the path to the ChromeDriver executable included with Chrome for Testing
    chromedriver_path = os.getenv('CHROME_DRIVER_PATH')
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver
