import requests
from selenium import webdriver

# Initialize Selenium webdriver
driver = webdriver.Chrome()

# Open the URL using Selenium
url = "https://sci-hub.se/"
driver.get(url)

# Get the current URL from Selenium
current_url = driver.current_url

# Send an HTTP request using requests library
response = requests.get(current_url)

# Get the HTTP response code
response_code = response.status_code

print("HTTP Response Code:", response_code)

# Close the Selenium webdriver
driver.quit()
