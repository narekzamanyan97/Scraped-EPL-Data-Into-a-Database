# !!! get the players of all the clubs from https://www.premierleague.com/players?se=363&cl=-1

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager

import time
import re

from set_up_driver import *

urls = {
	'url_1': 'https://www.premierleague.com/players?se=363&cl=-1',
}

# get the player's name, position, and country, then click on the row
def player_retrieve_1():
	# set up the driver
	driver = set_up_driver(urls['url_1'])

	# scroll down to the bottom of the page to include all the players
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	# there is a full screen ad on the page when we try to access the data
	#	with a webbot. close the ad before proceeding
	# find the close button for the ad
	advert = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//a[@id='advertClose']"))
	)
	print(0)
	ad_close_button = advert[0]
	# click on the close button
	print(1)
	driver.execute_script("arguments[0].click();", ad_close_button)

	print(2)
	# wait until the row of the last player on the list appears on the page
	# 	in 2020/2021 season, it is Martin Ødegaard, with the data-player='p184029'
	last_player = WebDriverWait(driver, 15).until(
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a/img[@data-player='p184029']"))
	)

	try:
		# get the player rows and links for the details
		player_rows = WebDriverWait(driver, 10).until(
				EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"))
		)

		player_row_buttons = WebDriverWait(driver, 10).until(
				EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a"))
		)

		players_list_of_dicts = []
		print(len(player_rows))
		print(len(player_row_buttons))

		counter = 0
		# get the basic player information from the rows
		for i in range(0, len(player_rows) - (len(player_rows) - 20)):
			# scroll down to the bottom of the page to include all the players
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			
			# make sure the 2020/2021 season table is loaded (instead of
			#	2021/22). check for the 2020/21 to appear
			# filter_2020_21 = WebDriverWait(driver, 20).until(
			# 	EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a/img[@data-player='p109646']"))
			# )
			# filter_2020_21 = WebDriverWait(driver, 10).until(
			# 	EC.presence_of_element_located((By.XPATH, '//div[@class="dropDown active"]/div[text() == "2020/21"]'))
			# )

			try:
				# find the close button for the ad after the page update
				advert = WebDriverWait(driver, 10).until(
					EC.presence_of_all_elements_located((By.XPATH, "//a[@id='advertClose']"))
				)  
				ad_close_button = advert[0]
				# click on the close button
				
				driver.execute_script("arguments[0].click();", ad_close_button)
			except TimeoutException:
				# in case there is no ad blocking the screen, continue with the 
				#	loop
				print('There is no ad. Proceed with the page!')
			print(2.5)
			# wait until the row of the last player on the list appears on the page
			# 	in 2020/2021 season, it is Martin Ødegaard, with the data-player='p184029'
			last_player = WebDriverWait(driver, 10).until(
				EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a/img[@data-player='p184029']"))
			)
			print(3)
			# get the player rows and links for the details after the page
			#	update
			player_rows = WebDriverWait(driver, 15).until(
					EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"))
			)
			print(3.5)
			player_row_buttons = WebDriverWait(driver, 10).until(
					EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a"))
			)
			print(4)

			temp_dict = {}

			print(len(player_rows))
			print(counter)
			counter += 1	

			tries = 0
			el_found = False
			while el_found == False:
				print(tries)
				try:
					player_row = player_rows[i].text
					el_found = True
				except StaleElementReferenceException:
					player_rows = WebDriverWait(driver, 10).until(
						EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"))
					)
					tries += 1

			player_row = player_rows[i].text

			player_row = player_row.splitlines()
			player_name = player_row[0]

			player_row = player_row[1].split()
			player_position = player_row[0]
			
			# get the country of the player: some player rows are missing the 
			#	country column
			try:
				player_country = player_row[1]
			except IndexError:
				player_country = 'Null'
			
			# add the player info to a dictionary
			temp_dict['player name'] = player_name
			temp_dict['position'] = player_position
			temp_dict['country'] = player_country
			# print(player_name)
			# add the player's detailed info to the temp_dict 
			player_details_dict = player_retrieve_2(driver, player_row_buttons[i])
			temp_dict.update(player_details_dict)
			print(temp_dict)
			# add the temp_dict to the list later to be returned from the function
			players_list_of_dicts.append(temp_dict)
			# print(players_list_of_dicts)
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
	# print(season_1.text)
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

# player_retrieve_1()