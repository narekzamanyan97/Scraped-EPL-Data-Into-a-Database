from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

all_seasons = ['1992/93', '1993/94', '1994/95', '1995/96', '1996/97', '1997/98',
		'1998/99', '1999/00', '2000/01', '2001/02', '2002/03', '2003/04', 
		'2004/05', '2005/06', '2006/07', '2007/08', '2008/09', '2009/10',
		'2010/11', '2011/12', '2012/13', '2013/14', '2014/15', '2015/16',
		'2016/17', '2017/18', '2018/19', '2019/20', '2020/21']

number_of_players_per_season = {'1992/93': 547, '1993/94': 0, '1994/95': 0,
		'1995/96': 0, '1996/97': 0, '1997/98': 0, '1998/99': 0, '1999/00': 0,
		'2000/01': 0, '2001/02': 0, '2002/03': 0, '2003/04': 0, '2004/05': 0,
		'2005/06': 0, '2006/07': 0, '2007/08': 0, '2008/09': 0, '2009/10': 0, 
		'2010/11': 0, '2011/12': 0, '2012/13': 0, '2013/14': 0, '2014/15': 0,
		'2015/16': 0, '2016/17': 0, '2017/18': 0, '2018/19': 0, '2019/20': 0,
		'2020/21': 861, '2021/22': 820}

# try and catch both timeout and stale element exceptions
# 	if index == -1, then don't handle stale element exception
# @returns:
#	if the index is -1
#		the entire web element
#	if the index is >= 0
#		the specified row
#   if the index is -2
#		return either after the ad element is found, or rethrow an exception
#		when there is a 
#		TimeoutException, because the script finds the ad very quickly, and 
#		since most of the time there is no ad, there is no need to try more than
#		once to find it, as the chances are it is not there.
#		Same with the shirt number, a lot of players don't have their
#		shirt number specified
def presence_of_all_el_located(driver, xpath, seconds_to_wait, index, season='2020/21'):
	tries = 0
	el_found = False
	
	num_of_player_rows = number_of_players_per_season[season]

	# handle TimeoutException
	while el_found == False and tries < 3:
		try:
			# # select the appropriate season from the dropdown
			# filter_season = WebDriverWait(driver, 15).until(
			# 		EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList']/li[@role='option' and text()='" + season  + "']"))
			# )
			
			# # choose the appropriate season from the dropdown list
			# driver.execute_script("arguments[0].click();", filter_season[0])
			
			element = WebDriverWait(driver, seconds_to_wait).until(
				EC.presence_of_all_elements_located((By.XPATH, xpath))
			)
			# make sure there are the right number of player rows before continuing
			if index >= -1 and len(element) == num_of_player_rows:
				el_found = True
				# print('element found **************************')
			elif index == -2:
				el_found = True
			else:
				print('----------------------------------------------')
				print(len(element))

				# scroll down to the bottom of the page to include all the players
				driver.refresh()
				time.sleep(5)

				# select the appropriate season from the dropdown
				filter_season = WebDriverWait(driver, 15).until(
						EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList']/li[@role='option' and text()='" + season  + "']"))
				)
				
				# choose the appropriate season from the dropdown list
				driver.execute_script("arguments[0].click();", filter_season[0])
				
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(5)
				print('******************* in presence_of_all_el_located ' + str(num_of_player_rows))
				

		except TimeoutException:
			tries += 1

			# if we are looking for an ad element, then pass the exception to the
			#	calling function so that we can move on
			if index == -2:
				raise TimeoutException('')

	# if we are tyring to find a specific element (index >= 0)
	if index != -1 and index != -2:
		tries = 0
		# handle stale element exception. If the element 
		el_not_stale = False
		while el_not_stale == False and tries < 3:
			try:
				el = element[index]
				# print(el.text)
				return el
			except StaleElementReferenceException:
				# in this case the element is stale, find it again
				element = WebDriverWait(driver, seconds_to_wait).until(
					EC.presence_of_all_elements_located((By.XPATH, xpath))
				)
				tries += 1
	else:
		return element


# check whether the has already been inserted into the database (whether it is
#		in list_of_players) or not
def is_player_new(list_of_players, player_name):
	try:
		# print(player_name)
		x = list_of_players.index(player_name)
		# print(player_name + " already exists.")
		return False
	except ValueError:
		return True