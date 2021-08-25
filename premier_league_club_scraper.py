# https://www.premierleague.com/clubs?se=363
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import Select

import time
import re

from set_up_driver import *

urls = {
	'url_1': 'https://www.premierleague.com/clubs?se=363',
}

# get the club's name and get the button to click to get the details
def club_retrieve_1():
	# set up the driver
	driver = set_up_driver(urls['url_1'])


	try:
		# get the club rows and links for the details
		club_rows_team = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='table']/table/tbody[@class='allTimeDataContainer']/tr/td[@class='team']/a/div[@class='nameContainer']"))
		)

		club_rows_venue = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='table']/table/tbody[@class='allTimeDataContainer']/tr/td[@class='venue']/a"))
		)

		# for i in range(0, len(club_rows_team)):
		# 	print(club_rows_team[i].text)
		# 	print(club_rows_venue[i].text)
		# 	print('------------------------------')

		clubs_list_of_dicts = []

		for i in range(12, len(club_rows_team) - (len(club_rows_team) - 14)):
			# again, get the player rows and links for the details
			club_rows_team = WebDriverWait(driver, 10).until(
					EC.presence_of_all_elements_located((By.XPATH, "//div[@class='table']/table/tbody[@class='allTimeDataContainer']/tr/td[@class='team']/a/div[@class='nameContainer']"))
			)

			club_rows_venue = WebDriverWait(driver, 10).until(
				EC.presence_of_all_elements_located((By.XPATH, "//div[@class='table']/table/tbody[@class='allTimeDataContainer']/tr/td[@class='venue']/a"))
			)

			temp_dict = {}

			# get the name of the club
			club_name = club_rows_team[i].text

			# get the name of the stadium
			stadium_name = club_rows_venue[i].text


			print(club_name + ':   ' + stadium_name)
			
			temp_dict['club name'] = club_name			
			temp_dict['stadium name'] = stadium_name

			# call club_retrieve_2() to get the website of the team
			temp_dict.update(club_retrieve_2(driver, club_rows_team[i]))

			clubs_list_of_dicts.append(temp_dict)

			# print the club info
			# for club_dict in clubs_list_of_dicts:
			for key, value in clubs_list_of_dicts[i - 12].items():
				print(key + '->' + value)

			print('--------------------------------------')

		driver.close()
		return clubs_list_of_dicts

	except TimeoutException as ex:
		print(str(ex))


# retrieve website name
def club_retrieve_2(driver, club_row):
	temp_dict = {}

	# click on the club row
	driver.execute_script("arguments[0].click();", club_row)

	# get the website name (some teams have no website)
	try:
		website = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='clubDetails']/div[@class='website']/a"))
		)
		website = website[0].text
		temp_dict['website'] = website
	except TimeoutException:
		temp_dict['website'] = 'Null'

	

	# call club_retrieve_3() to obtain the stadium information
	stadium_dict = club_retrieve_3(driver)

	temp_dict.update(stadium_dict)

	# go back to the previous page
	driver.execute_script("window.history.go(-1)")

	# return 2 dictionaries. one for the club details, another for stadium
	return temp_dict


# retrieve the stadium information
def club_retrieve_3(driver):
	# get the stadium button from the list of tabs
	stadium_button = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//nav[@class='heroPageLinks']/ul/li/a"))
	)

	# click on the stadium button
	driver.execute_script("arguments[0].click();", stadium_button[6])
	
	temp_dict = {}
	
	try:
		# get the stadium information button
		stadium_info_button = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='tablist']/li"))
		)

		# click on the stadium information button
		driver.execute_script("arguments[0].click();", stadium_info_button[1])
	
		# get the stadium details
		stadium_details = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='articleTabContent']/div[@class='articleTab active']/p"))
		)

		for detail in stadium_details:
			type_and_detail = detail.text.split(':')
			try:
				type_ = type_and_detail[0]
				type_ = type_.strip()
				# for consistency
				if type_ == 'Opened':
					type_ = 'Built'
				elif type_ == 'Tottenham Hotspur Stadium capacity':
					type_ = 'Capacity'

				detail = type_and_detail[1]

				# Fulham's stadium's capacity has text inside the parenthesis
				#	following the actual capacity.
				if '(due to' in detail:
					detail = detail.partition('(')[0]
				# Newcastle Utd's phone has exta info
				elif '(calls cost 7p per' in detail:
					detail = detail.partition('calls cost')[0]
				# Sheffield Utd also has unnecessary info
				elif 'John Street Stand' in detail:
					continue

				detail = detail.strip()

				temp_dict[type_] = detail
			except IndexError:
				break
	except TimeoutException:
		print('Club has no stadium information.')
		temp_dict['Capacity'] = 'Null'
		temp_dict['Record PL attendance'] = 'Null'
		temp_dict['Built'] = 'Null'
		temp_dict['Pitch size'] = 'Null'
		temp_dict['Stadium address'] = 'Null'
		temp_dict['Phone'] = 'Null'

	# go back to the previous page
	driver.execute_script("window.history.go(-1)")

	return temp_dict

# clubs = club_retrieve_1()