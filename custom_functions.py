from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

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
def presence_of_all_el_located(driver, xpath, seconds_to_wait, index, url_to_use=-1):
	tries = 0
	el_found = False
	
	num_of_player_rows = 0

	if url_to_use == 1:
		num_of_player_rows = 861
	elif url_to_use == 2:
		num_of_player_rows = 820

	# handle TimeoutException
	while el_found == False and tries < 3:
		try:
			element = WebDriverWait(driver, seconds_to_wait).until(
				EC.presence_of_all_elements_located((By.XPATH, xpath))
			)
			# make sure there are the right number of player rows before continuing
			if index >= -1 and len(element) == num_of_player_rows:
				el_found = True
			elif index == -2:
				el_found = True
			else:
				print('----------------------------------------------')
				print(len(element))
				# print(element[len(element) - 1].text)
				# print(element[0].text)
				# print(element[222].text)
				# print(element[444].text)

				# scroll down to the bottom of the page to include all the players
				driver.refresh()
				time.sleep(5)
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(5)
				print('******************* in presence_of_all_el_located ' + str(num_of_player_rows))
				

		except TimeoutException:
			tries += 1

			# if we are looking for an ad element, then pass the exception to the
			#	calling function so that we can move on
			if index == -2:
				raise TimeoutException('')

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
