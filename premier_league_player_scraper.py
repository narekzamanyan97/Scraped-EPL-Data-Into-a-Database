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

# get the player's name, position, and country, then click on the row
def player_retrieve_1():
	# set up the driver
	driver = set_up_driver(urls['url_1'])

	# scroll down to the bottom of the page to include all the players
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	# there is a full screen ad on the page when we try to access the data
	#	with a webbot. close the ad before proceeding
	# find the close button for the ad
	advert_xpath = "//a[@id='advertClose']"
	advert = presence_of_all_el_located(driver, advert_xpath, SECONDS_TO_WAIT, -1)
	ad_close_button = advert[0]
		
	# click on the close button
	driver.execute_script("arguments[0].click();", ad_close_button)

	# wait until the row of the last player on the list appears on the page
	# 	in 2020/2021 season, it is Martin Ødegaard, with the data-player='p184029'
	last_player_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a/img[@data-player='p184029']"
	last_player = presence_of_all_el_located(driver, last_player_xpath, SECONDS_TO_WAIT, -1)

	try:
		# get the player rows to start the for loop
		player_rows_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"
		player_rows = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, -1)

		players_list_of_dicts = []

		counter = 0

		# get the basic player information from the rows
		for i in range(60, len(player_rows) - (len(player_rows) - 70)):
			# scroll down to the bottom of the page to include all the players
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			
			# make sure the 2020/2021 season table is loaded (instead of
			#	2021/22). check for the 2020/21 to appear
			filter_2020_21 = WebDriverWait(driver, 20).until(
				EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a/img[@data-player='p109646']"))
			)

			# get the player_rows for the for loop, so we can count the
			#	number of players
			player_rows = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, -1)

			# wait until the row of the last player on the list appears on the page
			# 	in 2020/2021 season, it is Martin Ødegaard, with the data-player='p184029'
			last_player_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a/img[@alt='Photo for Martin Ødegaard']"
			last_player = presence_of_all_el_located(driver, last_player_xpath, SECONDS_TO_WAIT, -1)			

			# get the player rows and links for the details after the page
			#	update
			print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
			player_rows_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"
			player_row = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, i)
			print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

			player_row_buttons_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a"
			player_row_button = presence_of_all_el_located(driver, player_row_buttons_xpath, SECONDS_TO_WAIT, i)


			temp_dict = {}

			print(counter)
			counter += 1	

			# the player_rows frequently throws a stale element error.
			#	keep looking for the element (3 tries)
			player_row_text = player_row.text
			print(player_row_text)
			player_row_text_list = player_row_text.splitlines()
			player_name = player_row_text_list[0]

			player_position_and_country = player_row_text_list[1].split()
			player_position = player_position_and_country[0]
			
			# get the country of the player: some player rows are missing the 
			#	country column
			try:
				player_country = player_position_and_country[1]
			except IndexError:
				player_country = 'Null'
			
			# add the player info to a dictionary
			temp_dict['player name'] = player_name
			temp_dict['position'] = player_position
			temp_dict['country'] = player_country

			# add the player's detailed info to the temp_dict 
			player_details_dict = player_retrieve_2(driver, player_row_button)
			temp_dict.update(player_details_dict)
			print(temp_dict)
			# add the temp_dict to the list later to be returned from the function
			players_list_of_dicts.append(temp_dict)
			print('-----------------------------------------------------')

		# print(players_list_of_dicts)
		return players_list_of_dicts

	except TimeoutException as ex:
		print('')

# get the player's shirt number, club, date of birth, height, and club
def player_retrieve_2(driver, player_row_button):
	dict_to_return = {}


	# click on the player row to get more detailed information about the player
	driver.execute_script("arguments[0].click();", player_row_button)


	# get the player's number first
	try:
		player_number = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='wrapper playerContainer']/div[@class='playerDetails']/div[@class='number t-colour']"))
		)
		player_number = player_number[0].text


		dict_to_return['shirt number'] = player_number
	except TimeoutException:
		dict_to_return['shirt number'] = 'Null'

	# some player's have no club in the top left corner, so use the div in
	#	the center of the page to get the club of the player in 2020-2021
	#	season
	player_career = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='table playerClubHistory  true']/table/tbody/tr[@class='table']"))
	)

	# get the top two rows on the table, either of which contain the 
	#	2020/2021 and 2021/2022 seasons. 
	season_1 = player_career[0]
	season_1_list = season_1.text.splitlines()
	season_years = season_1_list[0]
	if season_years == '2020/2021':
		season_club = season_1_list[1]
	# if the top-most row is not 2020/2021, then the 2nd row should be 2020/2021
	else:
		# in case the player started in 2021/2022 season, he will not have
		#	a second row in player_career, so the index 1 can be out of range
		try:
			season_2 = player_career[1]
			# print(season_2.text)
			season_2_list = season_2.text.splitlines()
			season_years = season_2_list[0]
			season_club = season_2_list[1]
		except IndexError:
			season_club = 'Null'


	dict_to_return['club'] = season_club

	# Some players have no nationality
	try:
		personal_details = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='personalLists']/ul"))
		)

		# get the date of birth and height of the player
		date_of_birth = personal_details[1].text.splitlines()
		date_of_birth = date_of_birth[1].split()[0]
		dict_to_return['date of birth'] = date_of_birth

		# Some players have no height field
		try:
			height = personal_details[2].text.splitlines()
			height = height[1]
		except IndexError:
			height = 'Null'
		dict_to_return['height'] = height

	except TimeoutException:
		print('')

	# go back to the previous page
	driver.execute_script("window.history.go(-1)")

	return dict_to_return

# try and catch both timeout and stale element exceptions
# 	if index == -1, then don't handle stale element exception
# @returns:
#	if the index is -1
#		the entire web element
#	if the index is specified
#		the specified row
def presence_of_all_el_located(driver, xpath, seconds_to_wait, index):
	tries = 0
	el_found = False
	# handle TimeoutException
	while el_found == False and tries < 3:
		print('tries (TimeoutException loop): ' + str(tries))
		try:
			element = WebDriverWait(driver, seconds_to_wait).until(
				EC.presence_of_all_elements_located((By.XPATH, xpath))
			)
			el_found = True
		except TimeoutException:
			tries += 1
			print('Timeout Exception Occured')

	if index != -1:
		tries = 0
		# handle stale element exception. If the element 
		el_not_stale = False
		while el_not_stale == False and tries < 3:
			print('tries (StaleElementException loop): ' + str(tries))
			try:
				el = element[index]
				print(el.text)
				print('return el')
				return el
			except StaleElementReferenceException:
				# in this case the element is stale, find it again
				element = WebDriverWait(driver, seconds_to_wait).until(
					EC.presence_of_all_elements_located((By.XPATH, xpath))
				)
				tries += 1
				print('Stale Element Exception Occured')
	else:
		print('return the element list')
		return element

# player_retrieve_1()