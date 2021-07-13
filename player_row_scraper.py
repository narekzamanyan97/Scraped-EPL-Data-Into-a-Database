# !!! get the players of all the clubs from https://www.premierleague.com/players?se=363&cl=-1

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import time
import re

from set_up_driver import *

urls = {
	'url_1': 'https://www.premierleague.com/players?se=363&cl=-1',
}

SECONDS_TO_WAIT = 15

# this function retrieves all the player names from the rows of the
#	players page and appends them into a list, without clicking any of
#	the player rows. 
# the purpose is to have an ordered list with which the player_scraper
#	can compare its rows and avoid duplicates or miss players.
def get_all_the_player_rows():
	# set up the driver
	driver = set_up_driver(urls['url_1'])

	filter_2020_21 = WebDriverWait(driver, SECONDS_TO_WAIT).until(
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='current' and text()='2020/21']"))
	)

	print(filter_2020_21[0].text)

	# scroll down to the bottom of the page to include all the players
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(5)

	advert_xpath = "//a[@id='advertClose']"
	advert = WebDriverWait(driver, SECONDS_TO_WAIT).until(
		EC.presence_of_all_elements_located((By.XPATH, advert_xpath))
	)
	ad_close_button = advert[0]
		

	list_of_all_players_in_order = []

	# click on the close button
	driver.execute_script("arguments[0].click();", ad_close_button)
	time.sleep(5)

	# get the player rows to start the for loop
	player_rows_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"
	player_rows = WebDriverWait(driver, SECONDS_TO_WAIT).until(
		EC.presence_of_all_elements_located((By.XPATH, player_rows_xpath))
	)

	for player_row in player_rows:
		player_row_list = player_row.text.splitlines()
		player_name = player_row_list[0]

		player_position_and_country = player_row_list[1].split()
		try:
			player_position = player_position_and_country[0]
		except IndexError:
			player_position = '--------------------'
		
		try:
			player_country = player_position_and_country[1]
		except IndexError:
			player_country = '--------------------'

		print(player_name + '                  ' + player_position + '                   ' + player_country)

get_all_the_player_rows()