from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from set_up_driver import *
from helper_functions import *

SECONDS_TO_WAIT = 15

urls = {
	'url_all': 'https://www.premierleague.com/managers?se=-1&cl=-1',
	'url_1': 'https://www.premierleague.com/managers?se=363&cl=-1',
}

def manager_duplicate_check(season_index):
		# set up the driver
	driver = set_up_driver(urls['url_all'])





	managers_list_of_dicts = []

	counter = 0
	
	# iterate through the seasons
	for j in range(season_index, season_index + 1):
	
		# select the appropriate season from the dropdown
		filter_season = WebDriverWait(driver, 5).until(
			EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList']/li[@role='option' and text()='" + all_seasons[j]  + "']"))
		)

		# choose the appropriate season from the dropdown list
		driver.execute_script("arguments[0].click();", filter_season[0])
		
		time.sleep(5)

		all_seasons_managers =  WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//table/tbody[@class='dataContainer']/tr"))
		)

		# get the row manager id
		all_seasons_manager_ids =  WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//table/tbody[@class='dataContainer']/tr/td/a[@class='managerName']"))
		)

		# iterate through the managers
		for i in range(0, len(all_seasons_managers)):
			temp_dict = {}

			# get the row of the manager
			all_seasons_managers =  WebDriverWait(driver, 10).until(
				EC.presence_of_all_elements_located((By.XPATH, "//table/tbody[@class='dataContainer']/tr"))
			)

			# get the name button rows for the manager
			all_seasons_manager_button =  WebDriverWait(driver, 10).until(
				EC.presence_of_all_elements_located((By.XPATH, "//table/tbody[@class='dataContainer']/tr/td/a[@class='managerName']"))
			)

			manager_name = all_seasons_managers[i].text.splitlines()[0]

			temp_dict['manager name'] = manager_name
					
			# get the row manager id
			all_seasons_manager_ids =  WebDriverWait(driver, 10).until(
				EC.presence_of_all_elements_located((By.XPATH, "//table/tbody[@class='dataContainer']/tr/td/a[@class='managerName']"))
			)

			href = all_seasons_manager_ids[i].get_attribute('href')

			print(href)

			# get the id of the manager from the link
			href = href.split('managers/', 1)[1]
			manager_id = href.split('/')[0]

			print(manager_id)
			temp_dict['manager_id'] = manager_id

			managers_list_of_dicts.append(temp_dict)
			print(managers_list_of_dicts[counter])
			counter += 1
			print('----------------------------------')
		
	return managers_list_of_dicts


def all_seasons_manager_retrieve():
	# set up the driver
	driver = set_up_driver(urls['url_all'])

	all_seasons_managers =  WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//table/tbody[@class='dataContainer']/tr"))
	)

	# !!! change the season too to the one provided by the website

	managers_list_of_dicts = []

	counter = 0
	for i in range(10, len(all_seasons_managers)):
		temp_dict = {}

		# get the row of the manager
		all_seasons_managers =  WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//table/tbody[@class='dataContainer']/tr"))
		)

		# get the name button rows for the manager
		all_seasons_manager_button =  WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//table/tbody[@class='dataContainer']/tr/td/a[@class='managerName']"))
		)

		manager_name = all_seasons_managers[i].text.splitlines()[0]

		temp_dict['manager name'] = manager_name
		# print(temp_dict)
		temp_dict.update(manager_retrieve_2(driver, all_seasons_manager_button[i]))
		
		managers_list_of_dicts.append(temp_dict)
		print(managers_list_of_dicts[counter])
		counter += 1
		print('----------------------------------')
		
	return managers_list_of_dicts

# get the manager's name and club, then call another fucntion to get the
#	button to click to get the details
def manager_retrieve_1():
	# set up the driver
	driver = set_up_driver(urls['url_1'])
	
	managers_list_of_dicts = []
	
	for j in range(23, len(all_seasons)):
		print(all_seasons[j])
		counter = 0
		# select the previous season from the dropdown
		filter_season = WebDriverWait(driver, SECONDS_TO_WAIT).until(
				EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList']/li[@role='option' and text()='" + all_seasons[j]  + "']"))
		)

		# choose the appropriate season from the dropdown list
		driver.execute_script("arguments[0].click();", filter_season[0])	
		time.sleep(5)
		# get the manager rows and links for the details
		managers = WebDriverWait(driver, 10).until(														
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='table']/table/tbody[@class='dataContainer']/tr"))
		)

		# get the link to click to open the details page for the manager
		managers_button = WebDriverWait(driver, 10).until(														
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='table']/table/tbody[@class='dataContainer']/tr/td/a[@class='managerName']"))
		)

		print('--------------------------------')
		for i in range(0, len(managers)):
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
			temp_dict['season'] = all_seasons[j]

			# Since we are separating the logic of retrieve_manager_1 and all_seasons_manager_retrive,
			#		we don't need to call the retrieve_manager_2()
			# call manager_retrieve_2() which clicks on the manager row
			# temp_dict.update(manager_retrieve_2(driver, managers_button[i]))

			managers_list_of_dicts.append(temp_dict)
			
			print(managers_list_of_dicts[counter])
			counter += 1

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
		try:
			detail_list = detail.text.splitlines()
			if detail_list[0] != 'Age':
				if detail_list[0] == 'Premier League Debut Match':
					temp_dict[detail_list[0]] = detail_list[1] + detail_list[2]
				else:	
					temp_dict[detail_list[0]] = detail_list[1]
		except IndexError as ie:
			 print()
	print('-------------------------------')

	# print(temp_dict)

	# go back to the previous page
	driver.execute_script("window.history.go(-1)")

	return temp_dict

# all_seasons_manager_retrieve()
# manager_retrieve_1()
