from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os


CURRENT_DIR = os.path.dirname(os.path.abspath('__file__'))
chrome_path = os.path.join(CURRENT_DIR, 'chromedriver')

# add argument to driver options
chrome_options = Options()
# set headless so that chrome runs under the hood without popping up
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path=chrome_path,
                          options=chrome_options)
driver.get("https://duckduckgo.com")

# get the input form element with a given id
search_input = driver.find_element_by_xpath("(//input[contains(@class, 'js-search-input')])[1]")
# search_input = driver.find_element_by_id("search_form_input_homepage")
search_input.send_keys("My User Agent")


# search by pressing enter after typing text
search_input.send_keys(Keys.ENTER)

# search by clicking on the search button
# search_btn = driver.find_element_by_id("search_button_homepage")
# search_btn.click()

# when running under the hood, get the html content of the response
print(driver.page_source)

# close the driver to prevent accumulation of many python instances
driver.close()