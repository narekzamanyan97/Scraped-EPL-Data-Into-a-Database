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

import requests


# from premier_league_to_database import *
# from connect_to_database import *

# check the player_ids (data)

urls = {
	'url_1': 'https://www.premierleague.com/players',
	'url_2': 'https://www.premierleague.com/players?se=363&cl=-1',
}

SECONDS_TO_WAIT = 15

# !!! get the player id of each player, and their name, and check whether the player's
#		name already exists in player table, or if there is a duplicate. If there is,
#		then two> different players have the same name
def player_duplicate_check(season_index):
	driver = set_up_driver(urls['url_1'])

	players_dict = {}

	# !!!convert this function to check whether there are duplicates for managers too.

	# iterate over the seasons
	for j in range(season_index, season_index + 1):
		if all_seasons[j] < '1995/96':
			number_of_clubs = 22
		else:
			number_of_clubs = 20


		# iterate over the clubs
		for i in range(0, number_of_clubs):
			# select the appropriate season from the dropdown
			filter_season = WebDriverWait(driver, 5).until(
				EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList']/li[@role='option' and text()='" + all_seasons[j]  + "']"))
			)

			# choose the appropriate season from the dropdown list
			driver.execute_script("arguments[0].click();", filter_season[0])
			
			time.sleep(5)

			filter_club = WebDriverWait(driver, 5).until(
				EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList' and @data-dropdown-list='clubs']/li[@role='option' and @data-option-index=\"" + str(i) + "\"]"))
			)

			# choose the next club from the season
			driver.execute_script("arguments[0].click();", filter_club[0])
			time.sleep(5)

			# get the player rows and links for the details after the page
			#	update
			player_rows_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"

			# get the player_rows for the for loop, so we can count the
			#	number of players
			player_rows = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, -1, season=all_seasons[j], is_by_season_and_club=True)
			time.sleep(5)


			# get the player_id (data-player) provided by the website
			player_id_el = WebDriverWait(driver, 15).until(
				EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a/img"))
			)
			

			player_index = 0

			last_index = len(player_rows)

			# loop through the player rows and obtain player data
			while player_index < last_index:
				player_row = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, player_index, season=all_seasons[j], is_by_season_and_club=True)


				# get the text from the player row.
				player_row_text = player_row.text

				player_row_text_list = player_row_text.splitlines()
				player_name = player_row_text_list[0]
				player_position_and_country = player_row_text_list[1]
		

				player_id = player_id_el[player_index]

				# get the id of the player from the row
				player_id = player_id.get_attribute('data-player')

				print(player_name + '            ' + str(player_id) + '     ' + str(player_position_and_country))
				
				players_dict[player_id] = player_name

				player_index += 1
	return players_dict


def player_get_the_correct_country_and_position(season_index):
	driver = set_up_driver(urls['url_1'])

	players_dict = {}

	# iterate over the seasons
	for j in range(season_index, season_index + 1):
		if all_seasons[j] < '1995/96':
			number_of_clubs = 22
		else:
			number_of_clubs = 20

		# iterate over the clubs
		for i in range(0, number_of_clubs):
			# select the appropriate season from the dropdown
			filter_season = WebDriverWait(driver, 5).until(
				EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList']/li[@role='option' and text()='" + all_seasons[j]  + "']"))
			)

			# choose the appropriate season from the dropdown list
			driver.execute_script("arguments[0].click();", filter_season[0])
			
			time.sleep(5)

			filter_club = WebDriverWait(driver, 5).until(
				EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList' and @data-dropdown-list='clubs']/li[@role='option' and @data-option-index=\"" + str(i) + "\"]"))
			)

			# choose the next club from the season
			driver.execute_script("arguments[0].click();", filter_club[0])
			time.sleep(5)

			# get the player rows and links for the details after the page
			#	update
			player_rows_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"

			# get the player_rows for the for loop, so we can count the
			#	number of players
			player_rows = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, -1, season=all_seasons[j], is_by_season_and_club=True)
			time.sleep(5)


			# get the player_id (data-player) provided by the website
			player_id_el = WebDriverWait(driver, 15).until(
				EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a/img"))
			)
			

			player_index = 0

			last_index = len(player_rows)

			# loop through the player rows and obtain player data
			while player_index < last_index:
				player_row = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, player_index, season=all_seasons[j], is_by_season_and_club=True)


				# get the text from the player row.
				player_row_text = player_row.text

				player_row_text_list = player_row_text.splitlines()

				player_position_and_country = player_row_text_list[1]
						
				player_country = ''
				player_position = ''

				# truncate the position
				if 'Goalkeeper' in player_position_and_country:
					player_country = player_position_and_country.replace('Goalkeeper', '').strip()
					player_position = 'Goalkeeper'
				elif 'Defender' in player_position_and_country:
					player_country = player_position_and_country.replace('Defender', '').strip()
					player_position = 'Defender'
				elif 'Midfielder' in player_position_and_country:
					player_country = player_position_and_country.replace('Midfielder', '').strip()
					player_position = 'Midfielder'
				elif 'Forward' in player_position_and_country:
					player_country = player_position_and_country.replace('Forward', '').strip()
					player_position = 'Forward'
				else:
					player_country = player_position_and_country.strip()
					player_position = ''
					
					
				player_info = player_id_el[player_index]

				# get the id of the player from the row
				player_id = player_info.get_attribute('data-player')
				
				# get the small image url of the player
				player_40x40_img_url = player_info.get_attribute('src')
				
				# get the large 250x250 image url of the player by replacing the 40x40 found in the url
				#		with 250x250
				player_250x250_img_url = player_40x40_img_url.replace('40x40', '250x250')


				player_list = []
				player_list.append(player_country)
				player_list.append(player_position)
				player_list.append(player_40x40_img_url)
				player_list.append(player_250x250_img_url)
				print(str(player_id) + '-------------' + str(player_list) + '-------' + str(player_250x250_img_url))

				players_dict[player_id] = player_list

				player_index += 1

	return players_dict


def player_get_image_url(season_index):
	driver = set_up_driver(urls['url_1'])

	players_dict = {}

	# iterate over the seasons
	for j in range(season_index, season_index + 1):
		if all_seasons[j] < '1995/96':
			number_of_clubs = 22
		else:
			number_of_clubs = 20

		# iterate over the clubs
		for i in range(0, number_of_clubs):
			# select the appropriate season from the dropdown
			filter_season = WebDriverWait(driver, 5).until(
				EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList']/li[@role='option' and text()='" + all_seasons[j]  + "']"))
			)

			# choose the appropriate season from the dropdown list
			driver.execute_script("arguments[0].click();", filter_season[0])
			
			time.sleep(5)

			filter_club = WebDriverWait(driver, 5).until(
				EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList' and @data-dropdown-list='clubs']/li[@role='option' and @data-option-index=\"" + str(i) + "\"]"))
			)

			# choose the next club from the season
			driver.execute_script("arguments[0].click();", filter_club[0])
			time.sleep(5)

			# get the player rows and links for the details after the page
			#	update
			player_rows_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"

			# get the player_rows for the for loop, so we can count the
			#	number of players
			player_rows = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, -1, season=all_seasons[j], is_by_season_and_club=True)
			time.sleep(5)


			# get the player_id (data-player) provided by the website
			player_id_el = WebDriverWait(driver, 15).until(
				EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a/img"))
			)
			

			player_index = 0

			last_index = len(player_rows)

			# loop through the player rows and obtain player data
			while player_index < last_index:
				player_row = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, player_index, season=all_seasons[j], is_by_season_and_club=True)


				# get the text from the player row.
				player_row_text = player_row.text

				player_row_text_list = player_row_text.splitlines()			
					
				player_info = player_id_el[player_index]

				# get the id of the player from the row
				player_id = player_info.get_attribute('data-player')
				
				# get the small image url of the player
				player_40x40_img_url = player_info.get_attribute('src')
				
				# get the large 250x250 image url of the player by replacing the 40x40 found in the url
				#		with 250x250
				player_250x250_img_url = player_40x40_img_url.replace('40x40', '250x250')

				player_list = []
				player_list.append(player_40x40_img_url)
				player_list.append(player_250x250_img_url)
				print(str(player_id) + '-------------' + str(player_list) + '-------' + str(player_250x250_img_url))

				players_dict[player_id] = player_list

				player_index += 1

	return players_dict


# Since the image url of each player follows the same format, e.g.
#	https://resources.premierleague.com/premierleague/photos/players/250x250/p56981.png
#	with the only difference being the last part (before .png) that represents the player_id, and
#	the size of the image (either 40x40 or 250x250: if one exists, the other one also exists),
#	we can generate the url of images without scraping the premier league website.
#	Also, if a player has no image, then we have:
#		https://resources.premierleague.com/premierleague/photos/players/250x250/Photo-Missing.png
#	that is, we have Photo-Missing instead of the player_id at the end of the url string.
# @parameters:
#		list_of_player_ids = all the player_ids from player table
# @return
#		a list of dictionary with the elements being a dict of player id as the key and
#		the 40x40 and 250x250 image urls as the values
def player_generate_img_url(list_of_player_ids):
	player_id_img_dict = {}

	url_40x40_no_image = 'https://resources.premierleague.com/premierleague/photos/players/40x40/Photo-Missing.png'
	url_250x250_no_image = 'https://resources.premierleague.com/premierleague/photos/players/250x250/Photo-Missing.png'

	for player_id in list_of_player_ids:
		temp_list = []

		url_40x40 = 'https://resources.premierleague.com/premierleague/photos/players/40x40/' + player_id + '.png'
		url_250x250 = 'https://resources.premierleague.com/premierleague/photos/players/250x250/' + player_id + '.png'
		print('********************************************************************')
		response = requests.get(url_40x40)
		if response.status_code == 200:
			print('url exists')
			print(url_40x40)
			print(url_250x250)
			temp_list.append(url_40x40)
			temp_list.append(url_250x250)
		else:
			print('url does not exists')
			print(url_40x40)
			print(url_250x250)
			temp_list.append(url_40x40_no_image)
			temp_list.append(url_250x250_no_image)

		player_id_img_dict[player_id] = temp_list


def player_retrieve_by_season_and_club(player_club_list=[], season_index=0):
	driver = set_up_driver(urls['url_1'])

	unique_player_ids = []
	
	players_list_of_dicts = []

	# iterate over the seasons
	for j in range(season_index, season_index + 1):

		if all_seasons[j] < '1995/96':
			number_of_clubs = 22
		else:
			number_of_clubs = 20

		# iterate over the clubs
		for i in range(0, number_of_clubs):
			print('Season index = ' + str(season_index))
			# select the appropriate season from the dropdown
			filter_season = WebDriverWait(driver, 15).until(
				EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList']/li[@role='option' and text()='" + all_seasons[j]  + "']"))
			)

			# choose the appropriate season from the dropdown list
			driver.execute_script("arguments[0].click();", filter_season[0])
			
			print('after filter season')
			time.sleep(5)

			filter_club = WebDriverWait(driver, 15).until(
				EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList' and @data-dropdown-list='clubs']/li[@role='option' and @data-option-index=\"" + str(i) + "\"]"))
			)

			# choose the next club from the season
			driver.execute_script("arguments[0].click();", filter_club[0])
			time.sleep(5)

			# get the player rows and links for the details after the page
			#	update
			player_rows_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"

			# get the player_rows for the for loop, so we can count the
			#	number of players
			player_rows = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, -1, season=all_seasons[j], is_by_season_and_club=True)
			time.sleep(5)

			player_index = 0

			last_index = len(player_rows)

			print(last_index)
			

			# get the player_id (data-player) provided by the website
			player_id_els = WebDriverWait(driver, 15).until(
				EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a/img"))
			)

			# loop through the player rows and obtain player data
			while player_index < last_index:
				print('season index = ' + str(season_index))
				# select the appropriate season from the dropdown
				filter_season = WebDriverWait(driver, 15).until(
					EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList']/li[@role='option' and text()='" + all_seasons[j]  + "']"))
				)

				# choose the appropriate season from the dropdown list
				driver.execute_script("arguments[0].click();", filter_season[0])
				
				print('after filter season')
				time.sleep(5)

				filter_club = WebDriverWait(driver, 15).until(
					EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList' and @data-dropdown-list='clubs']/li[@role='option' and @data-option-index=\"" + str(i) + "\"]"))
				)

				# choose the next club from the season
				driver.execute_script("arguments[0].click();", filter_club[0])
				
				print('after filter club')
				time.sleep(5)


				player_row = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, player_index, season=all_seasons[j], is_by_season_and_club=True)




				# get the text from the player row.
				player_row_text = player_row.text

				player_row_text_list = player_row_text.splitlines()
				player_name = player_row_text_list[0]

				last_index = len(player_rows)

				print(last_index)

				# get the player_id (data-player) provided by the website
				player_id_els = WebDriverWait(driver, 15).until(
					EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a/img"))
				)

				# get the id of the current player
				player_id = player_id_els[player_index]

				# get the id of the player from the row
				player_id = player_id.get_attribute('data-player')

				print(player_name + '            ' + str(player_id))

				# !!! Change this so that you only check the player_id (provided by the website) rather than the name of the player 
				while (is_player_new(unique_player_ids, player_id) == False or is_player_data_in_player_club(player_club_list, player_id, all_seasons[j])) and player_index < last_index:
					print('season index = ' + str(season_index))
					print('*************** ' + player_id)
					# print so that we know the reason the code skips the player
					if is_player_new(unique_player_ids, player_id) == False and is_player_data_in_player_club(player_club_list, player_id, all_seasons[j]) == False:
						print('Player already retrieved.')
						did_duplicate_occur = True
					elif is_player_data_in_player_club(player_club_list, player_id, all_seasons[j]) == True:
						print('Player-season combination already in player_club.')
						print()

					player_index += 1

					if player_index < last_index:
						print('player_index = ' + str(player_index))
						print('last_index = ' + str(last_index))
			
						# get the next player row without refreshing the page.
						player_row = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, player_index, season=all_seasons[j], is_by_season_and_club=True)
						

						player_row_text = player_row.text

						player_row_text_list = player_row_text.splitlines()
						player_name = player_row_text_list[0]

						# get the next player's id without refreshing the page
						# get the player_id (data-player) provided by the website
						player_id_els = WebDriverWait(driver, 15).until(
							EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a/img"))
						)

						# get the id of the current player
						player_id = player_id_els[player_index]

						# get the id of the player from the row
						player_id = player_id.get_attribute('data-player')

					else:
						continue

				if player_index >= last_index:
					continue

			
				print('*************** ' + player_id)
				# check whether the player has not been retrieved yet.
				# 		if not, then append it to the unique_player_names and get the
				#		player data		 	
				unique_player_ids.append(player_id)

				player_position_and_country = player_row_text_list[1].split()
				player_position = player_position_and_country[0]
				
				# get the country of the player: some player rows are missing the 
				#	country column
				try:
					player_country = player_position_and_country[1]
				except IndexError:
					player_country = 'Null'
				
				temp_dict = {}

				# add the player info to a dictionary
				temp_dict['player id'] = player_id
				temp_dict['player name'] = player_name
				temp_dict['position'] = player_position
				temp_dict['country'] = player_country
				temp_dict['season'] = all_seasons[j]

				player_row_buttons_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a"
				player_row_button = presence_of_all_el_located(driver, player_row_buttons_xpath, SECONDS_TO_WAIT, player_index, season=all_seasons[j], is_by_season_and_club=True)
				
				# add the player's detailed info to the temp_dict 
				player_details_dict = player_retrieve_2(driver, player_row_button, all_seasons[j])

				temp_dict.update(player_details_dict)
				print(temp_dict)

				# add the temp_dict to the list later to be returned from the function
				players_list_of_dicts.append(temp_dict)
				player_index += 1

	print(players_list_of_dicts)
	return players_list_of_dicts

# @parameters:
#	player_club_list = all the rows of player_club used to check whether the player's
#		information is already in the database or not. If it is, do not click on
#		the player row button.
# get the player's name, position, and country, then click on the row
def player_retrieve_1(player_club_list, start_range):
	season_counter = -1

	unique_player_ids = []

	# Iterate over the seasons
	for j in range(start_range, start_range + 1):
		print(all_seasons[j])
		season_counter += 1



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
		stale_element_exception_occurred = True

		while stale_element_exception_occurred == True:
			try:
				player_rows = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, -1, season=all_seasons[j])
				stale_element_exception_occurred = False
			except StaleElementReferenceException:
				print('**********************************************Stale element exception.')


		players_list_of_dicts = []

		counter = 0

		# get the player_id (data-player) provided by the website
		player_id_els = WebDriverWait(driver, 15).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a/img"))
		)

		# Use this list to make sure no duplicate names are inserted into the 
		#	player table, as the scraper sometimes clicks on the same player row
		unique_player_ids = []

		original_row_amount = 0

		starting_counter = 52

		last_index = len(player_rows)

		i = starting_counter

		# iterate over the players
		while i < last_index:
			print(all_seasons[j])
			print('start_range = ' + str(start_range))
			print(len(player_rows))
			
			driver.refresh()

			# get the player_rows for the for loop, so we can count the
			#	number of players
			player_rows = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, -1, season=all_seasons[j])

			# get the player rows and links for the details after the page
			#	update
			player_rows_xpath = "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"
			
			last_index = len(player_rows)

			# often the number of rows found varies. The actual number is 863
			#	if the presence_of_all_el_located throws an IndexError
			#	(list index out of range), then we should refresh the page and
			#	try to scrape again to find the correct number of player rows
			try:
				player_row = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, i, season=all_seasons[j])
			except IndexError:
				print('continue*******************')
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
			stale_el_exc_occ = True
			while stale_el_exc_occ == True and i < last_index:
				player_row = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, i, season=all_seasons[j])
				try:
					player_row_text = player_row.text
					stale_el_exc_occ = False
				except StaleElementReferenceException:
					print('*******************************stale_el_exc_occ.')
				except AttributeError:
					print('*******************************AttributeError.')


			# get the player_id (data-player) provided by the website
			player_id_els = WebDriverWait(driver, 15).until(
				EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a/img"))
			)
			
			# get the id of the current player
			player_id = player_id_els[i]

			# get the id of the player from the row
			player_id = player_id.get_attribute('data-player')

			player_row_text_list = player_row_text.splitlines()
			player_name = player_row_text_list[0]

			print(player_name + '   ' + player_id)

			did_duplicate_occur = False

			# if the player has already been scraped, move on to the next player
			# 	or if the player_season combination (the club is not relevant) is
			#	already present in the player_club table, move on the the next player.
			while (is_player_new(unique_player_ids, player_id) == False or is_player_data_in_player_club(player_club_list, player_id, all_seasons[j])) and i < last_index:
				print(player_name + '   ' + player_id)
				# print so that we know the reason the code skips the player
				if is_player_new(unique_player_ids, player_id) == False and is_player_data_in_player_club(player_club_list, player_id, all_seasons[j]) == False:
					print('Player already retrieved.')
					did_duplicate_occur = True
				elif is_player_data_in_player_club(player_club_list, player_id, all_seasons[j]) == True:
					print('Player-season combination already in player_club.')
					print()

				i += 1
				print(i)
				
				if i < last_index:
					print('i = ' + str(i))
					print('last_index = ' + str(last_index))
					# get the next player row without refreshing the page.
					stale_el_exc = True
					while stale_el_exc == True and i < last_index:
						player_row = presence_of_all_el_located(driver, player_rows_xpath, SECONDS_TO_WAIT, i, season=all_seasons[j])
						try:
							player_row_text = player_row.text
							stale_el_exc = False
						except StaleElementReferenceException:
							print('************************************************Stale el exc.')
						except AttributeError:
							print()


					player_row_text_list = player_row_text.splitlines()
					player_name = player_row_text_list[0]


					# get the id of the current player
					player_id = player_id_els[i]

					# get the id of the player from the row
					player_id = player_id.get_attribute('data-player')

					# print(player_name)
				else:
					continue

			# make sure to exit the loop if the while loop above has incremented
			#		i above 
			if i >= last_index:
				continue
	
			# check whether the player has not been retrieved yet.
			# 		if not, then append it to the unique_player_names and get the
			#		player data		 	
			unique_player_ids.append(player_id)

			player_position_and_country = player_row_text_list[1]
			# player_position = player_position_and_country[0]
			
			# truncate the position
			if 'Goalkeeper' in player_position_and_country:
				player_country = player_position_and_country.replace('Goalkeeper', '').strip()
				player_position = 'Goalkeeper'
			elif 'Defender' in player_position_and_country:
				player_country = player_position_and_country.replace('Defender', '').strip()
				player_position = 'Defender'
			elif 'Midfielder' in player_position_and_country:
				player_country = player_position_and_country.replace('Midfielder', '').strip()
				player_position = 'Midfielder'
			elif 'Forward' in player_position_and_country:
				player_country = player_position_and_country.replace('Forward', '').strip()
				player_position = 'Forward'
			else:
				player_country = player_position_and_country.strip()
				player_position = ''

			print("********************************************")
			print(player_country)
			print(player_position)
			print("********************************************")
			
			temp_dict = {}

		
			counter += 1

			# add the player info to a dictionary
			temp_dict['player id'] = player_id
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