# !!! get the players of all the clubs from https://www.premierleague.com/players?se=363&cl=-1

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import time

from set_up_driver import *

from premier_league_player_scraper import *

from custom_functions import *

urls = {
	'url_1': 'https://www.premierleague.com/players',
	'url_2': 'https://www.premierleague.com/players?se=363&cl=-1',
}

SECONDS_TO_WAIT = 15

# this function retrieves all the player names from the rows of the
#	players page and appends them into a list, without clicking any of
#	the player rows. 
# the purpose is to have an ordered list with which the player_scraper
#	can compare its rows and avoid duplicates or miss players.
def get_all_the_player_rows(season):
	
	# set up the driver
	driver = set_up_driver(urls['url_1'])

	print('in get_all_the_player_rows')
	# if url_to_use == 1:
	# 	driver = set_up_driver(urls['url_1'])
	# 	num_of_player_rows = 861
	# else:
	# 	driver = set_up_driver(urls['url_2'])
	# 	num_of_player_rows = 820

	advert_xpath = "//a[@id='advertClose']"
	advert = WebDriverWait(driver, SECONDS_TO_WAIT).until(
		EC.presence_of_all_elements_located((By.XPATH, advert_xpath))
	)
	ad_close_button = advert[0]

	# click on the close button
	driver.execute_script("arguments[0].click();", ad_close_button)
	time.sleep(5)


	# select the appropriate season from the dropdown
	filter_season = WebDriverWait(driver, SECONDS_TO_WAIT).until(
			EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList']/li[@role='option' and text()='" + season  + "']"))
	)
	
	# choose the appropriate season from the dropdown list
	driver.execute_script("arguments[0].click();", filter_season[0])


	# scroll down to the bottom of the page to include all the players
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(5)


	list_of_all_players_in_order = []


	# get the player rows to start the for loop
	player_rows_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"

	player_rows = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, -1, season=season)

	# time.sleep(5)

	print(len(player_rows))
	print('before the for loop.')
	for i in range(0, len(player_rows)):
		try:
			# print('in the loop: ' + str(i))
			player_row_list = player_rows[i].text.splitlines()
			player_name = player_row_list[0]
			
			list_of_all_players_in_order.append(player_name)
		except StaleElementReferenceException:
			player_rows = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, -1, season=season)

	return list_of_all_players_in_order

# get_all_the_player_rows(1)
