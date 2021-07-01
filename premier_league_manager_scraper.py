# https://www.premierleague.com/managers?se=363&cl=-1
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
	'url_1': 'https://www.premierleague.com/managers?se=363&cl=-1',
}

# get the manager's name and club, then call another fucntion to get the
#	button to click to get the details
def manager_retrieve_1():
	# set up the driver
	driver = set_up_driver(urls['url_1'])

	# get the manager rows and links for the details
	managers = WebDriverWait(driver, 10).until(														
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='table']/table/tbody[@class='dataContainer']/tr"))
	)

	# get the link to click to open the details page for the manager
	managers_button = WebDriverWait(driver, 10).until(														
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='table']/table/tbody[@class='dataContainer']/tr/td/a[@class='managerName']"))
	)

	managers_list_of_dicts = []

	print('--------------------------------')
	for i in range(0, len(managers) - 22):
		temp_dict = {}

		# get the manager rows and links for the details to avoid
		#	stale element error
		managers = WebDriverWait(driver, 10).until(														
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='table']/table/tbody[@class='dataContainer']/tr"))
		)

		# get the link to click to open the details page for the manager
		managers_button = WebDriverWait(driver, 10).until(														
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='table']/table/tbody[@class='dataContainer']/tr/td/a[@class='managerName']"))
		)

		name_club_nation = managers[i].text
		name_club_nation_list = name_club_nation.splitlines()

		manager_name = name_club_nation_list[0]
		manager_club = name_club_nation_list[1]

		temp_dict['manager name'] = manager_name
		temp_dict['manager club'] = manager_club

		# call manager_retrieve_2() which clicks on the manager row
		temp_dict.update(manager_retrieve_2(driver, managers_button[i]))

		managers_list_of_dicts.append(temp_dict)
		
		# print(managers_list_of_dicts)

	print('--------------------------------')
	return managers_list_of_dicts

# get the details of the manager
def manager_retrieve_2(driver, button):
	# click on the manager's link
	driver.execute_script("arguments[0].click();", button)
	
	temp_dict = {}

	# get the link to click to open the details page for the manager
	manager_personal_details = WebDriverWait(driver, 10).until(														
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='personalLists']/ul/li"))
	)

	for detail in manager_personal_details:
		print(detail.text)
		try:
			detail_list = detail.text.splitlines()
			if detail_list[0] != 'Age':
				if detail_list[0] == 'Premier League Debut Match':
					temp_dict[detail_list[0]] = detail_list[1] + detail_list[2]
				else:	
					temp_dict[detail_list[0]] = detail_list[1]
		except IndexError as ie:
			 print(ie)
		print('-------------------------------')

	# print(temp_dict)

	# go back to the previous page
	driver.execute_script("window.history.go(-1)")

	return temp_dict

manager_retrieve_1()