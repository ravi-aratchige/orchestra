import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# ensure browser does not close after end of script execution
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# set up the Chromium web driver
driver = webdriver.Chrome(options=chrome_options)

# open the arXiv webpage
driver.get("https://arxiv.org/")
time.sleep(5)

# enter search query
search_field = driver.find_element(By.NAME, "query")
search_field.send_keys("Structural design patterns")
search_field.send_keys(Keys.RETURN)

time.sleep(10)
