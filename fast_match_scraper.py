from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import time
import re

from set_up_driver import *

from helper_functions import *

urls = {
	'url_1': 'https://www.premierleague.com/match/',
}

def result_scraper():
	driver = set_up_driver(urls['url_1'])

	for i in range(1, 10):
		driver.get(urls['url_1'] + str(i))

		# get attendance of the match
		attendance = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='attendance hide-m']"))
		)

		print(attendance[0].text)
		

result_scraper()