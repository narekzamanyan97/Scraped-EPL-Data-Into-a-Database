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

from helper_functions import *


# from premier_league_to_database import *
# from connect_to_database import *


urls = {
	'url_1': 'https://www.premierleague.com/players',
	'url_2': 'https://www.premierleague.com/players?se=363&cl=-1',
}

SECONDS_TO_WAIT = 15

# !!! add a parameter that includes all the players in the player_club table.
#		Then check whether the player's club data is in the player_club. If it is,
#		then skip the player. If it is not, then add all the season-club pairs.
# @parameters:
#	player_club_list = all the rows of player_club used to check whether the player's
#		information is already in the database or not. If it is, do not click on
#		the player row button.
# get the player's name, position, and country, then click on the row
def player_retrieve_1(player_club_list):
	season_counter = -1

	unique_player_names = []

	for j in range(4, len(all_seasons) - (len(all_seasons) - 5)):
		print(all_seasons[j])
		season_counter += 1

		# No need for this
		# call the get_all_the_player_rows() from player_row_scraper to
		#	get the correct order of all the players and check this scraper
		#	to match the correct order.
		# list_of_all_players_in_order = get_all_the_player_rows(all_seasons[j])
	
		# print('***********************')
		# print(len(list_of_all_players_in_order))


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

		# !!! make it so that all the season information is retrieved.
		#		then check the database whether that season is present in the
		#		player_club table. If it is, do not click on the player, just move
		#		on to the next player. If it is not, then click on the player and
		#		get all the season's information (the clubs he played for).

		# Use this list to make sure no duplicate names are inserted into the 
		#	player table, as the scraper sometimes clicks on the same player row
		unique_player_names = []

		original_row_amount = len(player_rows)

		starting_counter = 431
		last_index = 450

		i = starting_counter
		# get the basic player information from the 
		while i < len(player_rows) - (len(player_rows) - last_index):
			print(all_seasons[j])
			print(len(player_rows))

			driver.refresh()

			print(i)
			print(counter)

			# get the player_rows for the for loop, so we can count the
			#	number of players
			player_rows = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, -1, season=all_seasons[j])

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

			did_duplicate_occur = False

			# if the player has already been scraped, move on to the next player
			# 	or if the player_season combination (the club is not relevant) is
			#	already present in the player_club table, move on the the next player.
			while (is_player_new(unique_player_names, player_name) == False or is_player_data_in_player_club(player_club_list, player_name, all_seasons[j])) and i < last_index:
				
				# print so that we know the reason the code skips the player
				if is_player_new(unique_player_names, player_name) == False and is_player_data_in_player_club(player_club_list, player_name, all_seasons[j]) == False:
					print('Player already retrieved.')
					did_duplicate_occur = True
				elif is_player_data_in_player_club(player_club_list, player_name, all_seasons[j]) == True:
					print('Player-season combination already in player_club.')

				i += 1
				print(i)
				
				if i < last_index:
					# get the next player row without refreshing the page.
					player_row = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, i, season=all_seasons[j])
					player_row_text = player_row.text

					player_row_text_list = player_row_text.splitlines()
					player_name = player_row_text_list[0]
					print(player_name)

			# make sure to exit the loop if the while loop above has incremented
			#		i above 
			if i >= last_index:
				continue

			# check whether the player has not been retrieved yet.
			# 		if not, then append it to the unique_player_names and get the
			#		player data		 	
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
			temp_dict['season'] = all_seasons[j]

			player_row_buttons_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a"
			player_row_button = presence_of_all_el_located(driver, player_row_buttons_xpath, SECONDS_TO_WAIT, i, season=all_seasons[j])
			# add the player's detailed info to the temp_dict 
			player_details_dict = player_retrieve_2(driver, player_row_button, all_seasons[j])
			temp_dict.update(player_details_dict)
			print(temp_dict)
			# add the temp_dict to the list later to be returned from the function
			players_list_of_dicts.append(temp_dict)
			print('-----------------------------------------------------')

			if did_duplicate_occur == True and i < last_index:
				i = starting_counter
			else:
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
		# The current season may have two rows in case the player is transfered
		#		in the winter from one PL club to another.
		season_found_1 = False
		season_found_2 = False

		season_club_1 = 'Null'
		season_club_2 = 'Null'

		# !! changing the clubs_lists into a dictionary to store all seasons' data
		# 		for a player
		clubs_dict = {}

		# !!! add all the seasons to the dictionary
		for k in range(0, len(player_career)):
			# If the player is transfered from one PL club to another in the
			#		winter transfer window, then we must have two clubs for the 
			#		player for the same season. e.g. Olivier Giroud played both
			#		for Arsenal and Chelsea in 2017-2018 season.
			season_1 = player_career[k]
			season_1_list = season_1.text.splitlines()
			
			season_years = season_1_list[0]
			season_formatted = season_for_career_table[season]
			
			club_name_list = []
			club_name = season_1_list[1]

			club_name_list.append(club_name)
			# change the format of season_years from YYYY/YYYY to YYYY/YY
			season_years = season_years[:5] + season_years[7:]
			print(season_years + ' ' + club_name)



			# check whether the season is already in the dictionary. If it is,
			#		append the club of the season to the existing list.		
			if season_years in clubs_dict.keys():
				clubs_dict[season_years].append(club_name)
			else:
				clubs_dict[season_years] = club_name_list

	# Some players have no Career table populated
	except TimeoutException:
		print()
		clubs_dict = {}

	dict_to_return['clubs'] = clubs_dict

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
