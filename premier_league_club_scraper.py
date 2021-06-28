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
		# get the player rows and links for the details
		club_rows = WebDriverWait(driver, 10).until(
				EC.presence_of_all_elements_located((By.XPATH, "//div[@class='indexSection']/div/ul[@class='block-list-5 block-list-3-m block-list-1-s block-list-1-xs block-list-padding dataContainer']/li/a"))
		)

		clubs_list_of_dicts = []

		for i in range(0, len(club_rows)):
			# After we go pack to the previous page, it automatically takes
			#	us to the page for 2021-2022 season, and a few moments later,
			#	switches to 2020-2021 (the desired page).
			# Fulham does not appear in 2021-2022 club list as it was relegated. 
			# So wait until Fulham's logo appears before proceeding with the page
			fulham_logo = WebDriverWait(driver, 10).until(														
				EC.presence_of_all_elements_located((By.XPATH, "//img[@src='https://resources.premierleague.com/premierleague/badges/70/t54.png']"))
			)

			# again, get the player rows and links for the details
			club_rows = WebDriverWait(driver, 10).until(
					EC.presence_of_all_elements_located((By.XPATH, "//div[@class='indexSection']/div/ul[@class='block-list-5 block-list-3-m block-list-1-s block-list-1-xs block-list-padding dataContainer']/li/a"))
			)

			temp_dict = {}

			# get the name of the club
			club_name = club_rows[i].text.splitlines()[0]
			
			temp_dict['club name'] = club_name			

			# call club_retrieve_2() to get the website of the team
			temp_dict.update(club_retrieve_2(driver, club_rows[i]))

			clubs_list_of_dicts.append(temp_dict)

			print(clubs_list_of_dicts)
		
		for club_dict in clubs_list_of_dicts:
			for key, value in club_dict.items():
				print(key + '->' + value)

			print('--------------------------------------')

		return clubs_list_of_dicts

	except TimeoutException as ex:
		print(str(ex))


# retrieve website and stadium names
def club_retrieve_2(driver, club_row):
	temp_dict = {}

	# click on the club row
	driver.execute_script("arguments[0].click();", club_row)

	# get the stadium name
	stadium_name = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='clubDetails']/div[@class='stadiumName']/a/span[@class='stadium']"))
	)
	stadium_name = stadium_name[0].text.strip()

	temp_dict['stadium name'] = stadium_name

	# get the website name
	website = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='clubDetails']/div[@class='website']/a"))
	)

	website = website[0].text

	temp_dict['website'] = website

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

	temp_dict = {}
	
	for detail in stadium_details:
		type_and_detail = detail.text.split(':')
		try:
			type_ = type_and_detail[0]
			
			# for consistency
			if type_ == 'Opened':
				type_ = 'Built'

			detail = type_and_detail[1]

			detail = detail.strip()

			temp_dict[type_] = detail
		except IndexError:
			break

	# go back to the previous page
	driver.execute_script("window.history.go(-1)")

	return temp_dict

clubs = club_retrieve_1()