# !!! get the players of all the clubs from https://www.premierleague.com/players

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager

import time
import re

from set_up_driver import *

urls = {
	'url_1': 'https://www.premierleague.com/players',
}

# get the player's name, position, and country, then click on the row
def player_retrieve_1():
	# set up the driver
	driver = set_up_driver(urls['url_1'])

	# scroll down to the bottom of the page to include all the players
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(10)

	try:
		# get the player rows and links for the details
		player_rows = WebDriverWait(driver, 10).until(
				EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"))
		)

		player_row_buttons = WebDriverWait(driver, 10).until(
				EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a"))
		)

		players_list_of_dicts = []

		# get the basic player information from the rows
		for i in range(18, len(player_rows)):
			# scroll down to the bottom of the page to include all the players
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(10)
			
			player_rows = WebDriverWait(driver, 10).until(
					EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr"))
			)

			player_row_buttons = WebDriverWait(driver, 10).until(
					EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-12']/div[@class='table playerIndex']/table/tbody[@class='dataContainer indexSection']/tr/td/a"))
			)
			temp_dict = {}

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
				player_country = None
			
			# add the player info to a dictionary
			temp_dict['player name'] = player_name
			temp_dict['position'] = player_position
			temp_dict['country'] = player_country

			# add the player's detailed info to the temp_dict 
			player_details_dict = player_retrieve_2(driver, player_row_buttons[i])
			temp_dict.update(player_details_dict)
			
			# add the temp_dict to the list later to be returned from the function
			players_list_of_dicts.append(temp_dict)
			print(players_list_of_dicts)
			print('-----------------------------------------------------')



		# print(players_list_of_dicts)
		return players_list_of_dicts

	except TimeoutException as ex:
		print('')
			
# get the player's club, date of birth, height
def player_retrieve_2(driver, player_row_button):
	dict_to_return = {}

	# click on the player row to get more detailed information about the player
	driver.execute_script("arguments[0].click();", player_row_button)

	player_club = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//nav[@class='fixedSidebar']/div[@class='playerOverviewAside u-hide-mob']/section//div[@class='info']"))
	)
	club = player_club[0].text
	dict_to_return['club'] = club

	# Some players have no nationality
	try:
		personal_details = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='personalLists']/ul"))
		)

		# get the date of birth and height of the player
		# nationality = personal_details[0].text.splitlines()
		# nationality = nationality[1]
		# print('Nationality: ' + str(nationality))
		date_of_birth = personal_details[1].text.splitlines()
		date_of_birth = date_of_birth[1].split()[0]
		dict_to_return['date of birth'] = date_of_birth

		# Some players have no height field
		try:
			height = personal_details[2].text.splitlines()
			height = height[1]
		except IndexError:
			height = None
		dict_to_return['height'] = height

	except TimeoutException:
		print('')

	# go back to the previous page
	driver.execute_script("window.history.go(-1)")

	return dict_to_return

# player 			+
# position 			+
# nationality		+
# club
# date of birth
# height

# calculate and add to the database the goals, own goals, yellow cards, red cards,
# 	clean sheats, assists, appearances, wins, losses, draws


player_retrieve_1()