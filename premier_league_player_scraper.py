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

from player_row_scraper import *

from custom_functions import *


# from premier_league_to_database import *
# from connect_to_database import *


urls = {
	'url_1': 'https://www.premierleague.com/players',
	'url_2': 'https://www.premierleague.com/players?se=363&cl=-1',
}

SECONDS_TO_WAIT = 15

# get the player's name, position, and country, then click on the row
# @parameters:
#	url_to_use specifies whether we want the 2020/21 or 2021/22 player
#		page
# 	list_of_all_inserted_players is an array of all the players that are
#		already in the database so that we can save time and skip them
def player_retrieve_1(url_to_use, list_of_all_inserted_players):
	season_counter = -1

	for j in range(27, len(all_seasons)):
		print(all_seasons[j])
		season_counter += 1
		# call the get_all_the_player_rows() from player_row_scraper to
		#	get the correct order of all the players and check this scraper
		#	to match the correct order.
		list_of_all_players_in_order = get_all_the_player_rows(url_to_use, all_seasons[j])
	
		print('***********************')
		print(len(list_of_all_players_in_order))


		# set up the driver
		driver = set_up_driver(urls['url_1'])

		# scroll down to the bottom of the page to include all the players
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# there is a full screen ad on the page when we try to access the data
		#	with a webbot. close the ad before proceeding
		# find the close button for the ad
		advert_xpath = "//a[@id='advertClose']"
		advert = presence_of_all_el_located(driver, advert_xpath, SECONDS_TO_WAIT, -2)
		ad_close_button = advert[0]
			
		# click on the close button
		driver.execute_script("arguments[0].click();", ad_close_button)

		# get the player rows to start the for loop
		player_rows_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"
		player_rows = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, -1, season=all_seasons[j])

		players_list_of_dicts = []

		counter = 0

		# Use this list to make sure no duplicate names are inserted into the 
		#	player table, as the scraper sometimes clicks on the same player row
		unique_player_names = []

		original_row_amount = len(player_rows)



		i = len(player_rows) - 1
		# get the basic player information from the 
		while i < len(player_rows):
			print(all_seasons[j])

			driver.refresh()

			print(i)
			print(counter)

			# get the player_rows for the for loop, so we can count the
			#	number of players
			player_rows = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, -1, season=all_seasons[j])

			# wait until the row of the last player on the list appears on the page
			# 	in 2020/2021 season, it is Martin Ødegaard, with the data-player='p184029'
			# print('line 101')
			# last_player_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a/img[@alt='Photo for Martin Ødegaard']"
			# last_player = presence_of_all_el_located(driver, last_player_xpath, SECONDS_TO_WAIT, -1)			

			# get the player rows and links for the details after the page
			#	update
			player_rows_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"
			
			# often the number of rows found varies. The actual number is 863
			#	if the presence_of_all_el_located throws an IndexError
			#	(list index out of range), then we should refresh the page and
			#	try to scrape again to find the correct number of player rows
			try:
				player_row = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, i, season=all_seasons[j])
			except IndexError:
				continue

			# exit the advertisement screen
			try:
				advert_xpath = "//a[@id='advertClose']"
				advert = presence_of_all_el_located(driver, advert_xpath, SECONDS_TO_WAIT, -2)
				ad_close_button = advert[0]
			except TimeoutException:
				print('There is no advertisement button. Moving on!')

			# !!! The scraper jumps on players, or counts the same player twice.
			#	check whether the name of the player has aleary appeared or not
			#	if it did, go to the start of the loop and try again, 
			
			#	decrementing the counter by 1.
			# the player_rows frequently throws a stale element error.
			#	keep looking for the element (3 tries)
			# Sometimes player_row.text throws a StaleElementReferenceException
			#	even though it was tested in the function presence_of_all_el_located
			#	above. So the returned element is stale, even though it was not
			#	stale right before returing it from the function
			# Try and catch the exception, and call the funciton in the catch (except) 
			try:
				player_row_text = player_row.text
			except StaleElementReferenceException:
				player_row = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, i, season=all_seasons[j])
				player_row_text = player_row.text
			except AttributeError:
				player_row = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, i, season=all_seasons[j])
				player_row_text = player_row.text

			player_row_text_list = player_row_text.splitlines()
			player_name = player_row_text_list[0]

			# Checks whether the player is already inserted into the database.
			#		if it is, then increment the counter and check the next
			#		player on the player rows without refreshing the page.
			while is_player_new(list_of_all_inserted_players, player_name) != True:
				print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
				print(player_name)
				print('Player already in database')

				i += 1

				player_row = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, i, season=all_seasons[j])
				player_row_text = player_row.text
				player_row_text_list = player_row_text.splitlines()
				player_name = player_row_text_list[0]

			# Check whether the player found in this row matches the player that
			#		is supposed to be there. If not, then go back to the main loop
			#		and scrape the page again.
			if player_name != list_of_all_players_in_order[i]:
				# 	i += 1
				print('Index Pointing to Wrong Player. Try Again!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
				continue		 	

			unique_player_names.append(player_name)

			player_position_and_country = player_row_text_list[1].split()
			player_position = player_position_and_country[0]
			
			# get the country of the player: some player rows are missing the 
			#	country column
			try:
				player_country = player_position_and_country[1]
			except IndexError:
				player_country = 'Null'
			
			temp_dict = {}

		
			counter += 1

			# add the player info to a dictionary
			temp_dict['player name'] = player_name
			temp_dict['position'] = player_position
			temp_dict['country'] = player_country

			player_row_buttons_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a"
			player_row_button = presence_of_all_el_located(driver, player_row_buttons_xpath, SECONDS_TO_WAIT, i, season=all_seasons[j])
			# add the player's detailed info to the temp_dict 
			player_details_dict = player_retrieve_2(driver, player_row_button, all_seasons[j])
			temp_dict.update(player_details_dict)
			print(temp_dict)
			# add the temp_dict to the list later to be returned from the function
			players_list_of_dicts.append(temp_dict)
			print('-----------------------------------------------------')

			i += 1

	return players_list_of_dicts

# get the player's shirt number, club, date of birth, height, and club
def player_retrieve_2(driver, player_row_button, season):
	dict_to_return = {}


	# click on the player row to get more detailed information about the player
	driver.execute_script("arguments[0].click();", player_row_button)


	# get the player's number first
	try:
		player_number_xpath = "//div[@class='wrapper playerContainer']/div[@class='playerDetails']/div[@class='number t-colour']"
		player_number = presence_of_all_el_located(driver, player_number_xpath, SECONDS_TO_WAIT, -2)
		player_number = player_number[0].text
		dict_to_return['shirt number'] = player_number
	except TimeoutException:
		print('Player has no specified shirt number.')
	except IndexError:
		dict_to_return['shirt number'] = 'Null'

	# some player's have no club in the top left corner, so use the div in
	#	the center of the page to get the club of the player in 2020-2021
	#	season
	# player_career_xpath = "//div[@class='table playerClubHistory  true']/table/tbody/tr[@class='table']"
	# player_career = presence_of_all_el_located(driver, player_number_xpath, SECONDS_TO_WAIT, -1)
	try:
		player_career = WebDriverWait(driver, SECONDS_TO_WAIT).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@data-script='pl_player']/table/tbody/tr[@class='table']"))
		)

		# get the row of the table that contains the appropriate season

		# iterate through the player_career rows to find the one with the current
		#		season
		season_found = False
		for k in range(0, len(player_career)):
			# !!! If the player is transfered from one PL club to another in the
			#		winter transfer window, then we must have two clubs for the 
			#		player for the same season. e.g. Olivier Giroud played both
			#		for Arsenal and Chelsea in 2017-2018 season.
			season_1 = player_career[k]
			season_1_list = season_1.text.splitlines()
			print(season_1_list)
			season_years = season_1_list[0]
			season_formatted = season_for_career_table[season]
			if season_years == season_formatted:
				season_found = True
				season_club = season_1_list[1]
				break
				
			# # if the top-most row is not 2020/2021, then the 2nd row should be 2020/2021
			# else:
			# 	# in case the player started in 2021/2022 season, he will not have
			# 	#	a second row in player_career, so the index 1 can be out of range
			# 	try:
			# 		season_2 = player_career[1]
			# 		season_2_list = season_2.text.splitlines()
			# 		season_years = season_2_list[0]
			# 		season_club = season_2_list[1]
			# 	except IndexError:
			# 		season_club = 'Null'

		if season_found == False:
			season_club = 'Null'
	# !!! The club is taken from 2020/21 season. change that to reflect the appropriate
	#		season
		
	# Some players, such as Junior Firpo, have no Career table populated
	except TimeoutException:
		season_club = 'Null'

	dict_to_return['club'] = season_club

	# Some players have no nationality
	try:
		personal_details_xpath = "//div[@class='personalLists']/ul"
		personal_details = presence_of_all_el_located(driver, personal_details_xpath, SECONDS_TO_WAIT, -2)

		# get the date of birth and height of the player
		try:
			date_of_birth = personal_details[1].text.splitlines()
			date_of_birth = date_of_birth[1].split()[0]
			dict_to_return['date of birth'] = date_of_birth
		except IndexError:
			dict_to_return['date of birth'] = '0000-00-00'

		# Some players have no height field
		try:
			height = personal_details[2].text.splitlines()
			height = height[1]
		except IndexError:
			height = 'Null'
	# catch the rethrown TimeoutException. Some players have no personal details
	#	division on the screen
	except TimeoutException:
		print('No details division.')
		dict_to_return['date of birth'] = '0000-00-00'
		height = 'Null'

	dict_to_return['height'] = height

	# go back to the previous page
	driver.execute_script("window.history.go(-1)")

	return dict_to_return


# Jan Bednarek plays in Southampton