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
	'url_1': 'https://www.premierleague.com/players?se=363&cl=-1',
	'url_2': 'https://www.premierleague.com/players'
}

SECONDS_TO_WAIT = 15

# this function retrieves all the player names from the rows of the
#	players page and appends them into a list, without clicking any of
#	the player rows. 
# the purpose is to have an ordered list with which the player_scraper
#	can compare its rows and avoid duplicates or miss players.
def get_all_the_player_rows(url_to_use):
	
	# set up the driver
	if url_to_use == 1:
		driver = set_up_driver(urls['url_1'])
		num_of_player_rows = 861
	else:
		driver = set_up_driver(urls['url_2'])
		num_of_player_rows = 820

	advert_xpath = "//a[@id='advertClose']"
	advert = WebDriverWait(driver, SECONDS_TO_WAIT).until(
		EC.presence_of_all_elements_located((By.XPATH, advert_xpath))
	)
	ad_close_button = advert[0]

	# click on the close button
	driver.execute_script("arguments[0].click();", ad_close_button)
	time.sleep(5)


	if url_to_use == 1:
		filter_2020_21 = WebDriverWait(driver, SECONDS_TO_WAIT).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='current' and text()='2020/21']"))
		)
	else:
		filter_2021_22 = WebDriverWait(driver, SECONDS_TO_WAIT).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='current' and text()='2021/22']"))
		)

	# scroll down to the bottom of the page to include all the players
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(5)


	list_of_all_players_in_order = []


	# get the player rows to start the for loop
	player_rows_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"
	
	player_rows = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, -1, url_to_use)

	print(len(player_rows))
	while len(player_rows) != num_of_player_rows:
		print('----------------------------------------------------')
		print(len(player_rows))
		print(player_rows[len(player_rows) - 1].text)
		print(player_rows[0].text)
		print(player_rows[222].text)
		print('Wrong number of player rows. Try Again!')
		
		# refresh the page
		driver.refresh()

		# scroll down to the bottom of the page to include all the players
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(5)
		player_rows = premier_league_player_scraper.presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, -1, url_to_use)
		print('----------------------------------------------------')

	time.sleep(5)

	print(len(player_rows))
	for i in range(0, len(player_rows)):
		player_row_list = player_rows[i].text.splitlines()
		player_name = player_row_list[0]
		
		list_of_all_players_in_order.append(player_name)

	return list_of_all_players_in_order

# get_all_the_player_rows(1)