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
		'2016/17', '2017/18', '2018/19', '2019/20', '2020/21', '2021/22']

number_of_players_per_season = {'1992/93': 547, '1993/94': 563, '1994/95': 571,
		'1995/96': 568, '1996/97': 571, '1997/98': 602, '1998/99': 606, '1999/00': 664,
		'2000/01': 666, '2001/02': 666, '2002/03': 755, '2003/04': 773, '2004/05': 727,
		'2005/06': 701, '2006/07': 738, '2007/08': 762, '2008/09': 792, '2009/10': 811, 
		'2010/11': 836, '2011/12': 827, '2012/13': 814, '2013/14': 803, '2014/15': 660,
		'2015/16': 690, '2016/17': 660, '2017/18': 793, '2018/19': 860, '2019/20': 969,
		'2020/21': 861, '2021/22': 820}

season_for_career_table = {'1992/93': '1992/1993', '1993/94': '1993/1994', '1994/95': '1994/1995',
		'1995/96': '1995/1996', '1996/97': '1996/1997', '1997/98': '1997/1998', '1998/99': '1998/1999', '1999/00': '1999/2000',
		'2000/01': '2000/2001', '2001/02': '2001/2002', '2002/03': '2002/2003', '2003/04': '2003/2004', '2004/05': '2004/2005',
		'2005/06': '2005/2006', '2006/07': '2006/2007', '2007/08': '2007/2008', '2008/09': '2008/2009', '2009/10': '2009/2010', 
		'2010/11': '2010/2011', '2011/12': '2011/2012', '2012/13': '2012/2013', '2013/14': '2013/2014', '2014/15': '2014/2015',
		'2015/16': '2015/2016', '2016/17': '2016/2017', '2017/18': '2017/2018', '2018/19': '2018/2019', '2019/20': '2019/2020',
		'2020/21': '2020/2021', '2021/22': '2021/2022'}

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

	# define a variable that holds an approximation of how low the number of rows
	#		can be. Since it is hard to load a page that has exactly num_of_player_rows
	#		number of rows, we can allow for little less, and not spend too much time
	#		on the loop below
	margin_of_error = num_of_player_rows - (num_of_player_rows/10)

	# handle TimeoutException
	while el_found == False and tries < 3:
		try:
			element = WebDriverWait(driver, seconds_to_wait).until(
				EC.presence_of_all_elements_located((By.XPATH, xpath))
			)

			# make sure there are the right number of player rows before continuing
			if index >= -1 and len(element) >= num_of_player_rows - margin_of_error:
				el_found = True
			elif index == -2:
				el_found = True
			else:
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
		x = list_of_players.index(player_name)
		return False
	except ValueError:
		return True