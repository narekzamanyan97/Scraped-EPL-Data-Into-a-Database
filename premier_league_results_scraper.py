# https://www.premierleague.com/results

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import time
import re

from set_up_driver import *

from custom_functions import *

urls = {
	'url_1': 'https://www.premierleague.com/results?co=1&se=363&cl=-1',
}

# retrieve the team names, score, the stadium name, and its city
# 	Argument:
#		list of all the match_ids available in the table. This is to save time
#		and skip over the match_ids that have already been considered before
def results_retrieve_1(all_match_ids):
	driver = set_up_driver(urls['url_1'])

	# iterate over the seasons
	for j in range(len(all_seasons) - 2, len(all_seasons) - 1):
		try:
			print(all_seasons[j])
			# select the appropriate season from the dropdown
			filter_season = WebDriverWait(driver, 15).until(
					EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList']/li[@role='option' and text()='" + all_seasons[j]  + "']"))
			)
			
			# choose the appropriate season from the dropdown list
			driver.execute_script("arguments[0].click();", filter_season[0])

			# Scroll down to load more results to include all the results
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(5)

			# Stadiums contains the following information:
			# 	stadium_name
			#	city
			stadiums = WebDriverWait(driver, 10).until(
				EC.presence_of_all_elements_located((By.XPATH, "//li[@class='matchFixtureContainer']/div[@class='fixture postMatch']/span[@class='overview']/span[@class='stadiumName']"))
			)

			# Find the list of results on the page
			# The results contains the following information:
			# 	team_name_1 
			# 	team_1_goals-team_2_goals
			#	team_name_2
			results = WebDriverWait(driver, 10).until(
				EC.presence_of_all_elements_located((By.XPATH, "//li[@class='matchFixtureContainer']/div[@class='fixture postMatch']/span[@class='overview']/span[@class='teams']"))
			)

			# Since the browser duplicates result rows when scrolling down, we need to use the ids
			#	of the rows on the page
			div_ids = WebDriverWait(driver, 10).until(
				EC.presence_of_all_elements_located((By.XPATH, "//li[@class='matchFixtureContainer']/div[@class='fixture postMatch']"))
			)

			number_of_results = len(results)
			number_of_stadiums = len(stadiums)
			print(number_of_results)
			
			counter = 1

			unique_ids = []

			number_of_results = len(div_ids)

			# holds all the results
			results_list_of_dicts = []
			results_list_of_list_of_dicts = []

			original_len_results = len(results)
			

			# make sure the script gets >= 380 (# of matches in a premier league season)
			#	results before proceeding
			# or >= 462 results for matches in season <= 1994/95
			if all_seasons[j] <= '1994/95':
				number_of_matchweeks = 462
			else:
				number_of_matchweeks = 380
			while len(results) < number_of_matchweeks:
				driver.refresh()
				time.sleep(5)
				print(len(results))
				# scroll down to the bottom of the page to include all the players
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(5)
				results = WebDriverWait(driver, 10).until(
					EC.presence_of_all_elements_located((By.XPATH, "//li[@class='matchFixtureContainer']/div[@class='fixture postMatch']/span[@class='overview']/span[@class='teams']"))
				)
				
			original_len_results = len(results)
			print('original results: ' + str(len(results)))
			# 	stadiums = WebDriverWait(driver, 10).until(
			# 		EC.presence_of_all_elements_located((By.XPATH, "//li[@class='matchFixtureContainer']/div[@class='fixture postMatch']/span[@class='overview']/span[@class='stadiumName']"))
			# 	)
			# 	results = WebDriverWait(driver, 10).until(
			# 		EC.presence_of_all_elements_located((By.XPATH, "//li[@class='matchFixtureContainer']/div[@class='fixture postMatch']/span[@class='overview']/span[@class='teams']"))
			# 	)

			# time.sleep(5)
			
			# Iterating over the results to get the team names, scores, stadium names,
			#	and then click at each result to get the details of the match
			i = 3

			num_of_unique_ids = 0
			while i < 5:
				# select the appropriate season from the dropdown
				filter_season = WebDriverWait(driver, 15).until(
						EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList']/li[@role='option' and text()='" + all_seasons[j]  + "']"))
				)
				
				# choose the appropriate season from the dropdown list
				driver.execute_script("arguments[0].click();", filter_season[0])
	
				print('*******************************' + str(num_of_unique_ids))
				duplicate_result_flag = False		
			
				# Scroll down to load more results to include all the results
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(5)
				
				# # make sure the script gets 380 (# of matches in a premier league season)
				# #	results before proceeding
				results = WebDriverWait(driver, 10).until(
					EC.presence_of_all_elements_located((By.XPATH, "//li[@class='matchFixtureContainer']/div[@class='fixture postMatch']/span[@class='overview']/span[@class='teams']"))
				)
				while len(results) < original_len_results:
					driver.refresh()
					time.sleep(5)
					print(len(results))
					# scroll down to the bottom of the page to include all the players
					driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					time.sleep(5)

					stadiums = WebDriverWait(driver, 10).until(
						EC.presence_of_all_elements_located((By.XPATH, "//li[@class='matchFixtureContainer']/div[@class='fixture postMatch']/span[@class='overview']/span[@class='stadiumName']"))
					)
					results = WebDriverWait(driver, 10).until(
						EC.presence_of_all_elements_located((By.XPATH, "//li[@class='matchFixtureContainer']/div[@class='fixture postMatch']/span[@class='overview']/span[@class='teams']"))
					)


				# Since the page is updated (after clicking on a link and going back), we need to
				#	find the result elements again
				stadiums = WebDriverWait(driver, 10).until(
					EC.presence_of_all_elements_located((By.XPATH, "//li[@class='matchFixtureContainer']/div[@class='fixture postMatch']/span[@class='overview']/span[@class='stadiumName']"))
				)
				results = WebDriverWait(driver, 10).until(
					EC.presence_of_all_elements_located((By.XPATH, "//li[@class='matchFixtureContainer']/div[@class='fixture postMatch']/span[@class='overview']/span[@class='teams']"))
				)
				div_ids = WebDriverWait(driver, 10).until(
					EC.presence_of_all_elements_located((By.XPATH, "//li[@class='matchFixtureContainer']/div[@class='fixture postMatch']"))
				)

				try:
					id = div_ids[i].get_attribute("data-matchid")
				except IndexError:
					break

				id = int(id)
				print(i)
				print('results ' + str(len(results)))

				# The rows of the page are being duplicated after the scrollTo
				# So we check whether the row has already appeared on the page or not
				while is_row_new(unique_ids, id) != True or is_row_new(all_match_ids, id) != True:
					duplicate_result_flag = True
					if i < original_len_results and i < 5:
						i += 1
						print(i)
						print(str(id) + ' exists.')
						try:
							id = div_ids[i].get_attribute("data-matchid")
							id = int(id)
						except IndexError:
							break

				if i < original_len_results and i < 5:
					# holds a result information
					result_dict = {}
					result_dict['match id'] = id

					# add the season to the result_dict
					result_dict['season'] = all_seasons[j]

					num_of_unique_ids += 1

					unique_ids.append(id)
					# truncated is an array of strings with the following format:
					# ['team_name_1', 'team_1_goals-team_2_goals', 'team_name_2']
					# truncated = result.text.splitlines()
					truncated = results[i].text.splitlines()

					# since the team names are the short versions, ignore them
					#	on the scoresheet. Only retrieve the scores
					scoresheet = truncated[1]

					# scores is an array of 2 elements with the number of goals for each
					# 	team. e.g. ['2-0']
					scores = scoresheet.splitlines()
					# scores now is an array with the number of goals as its elements
					#	e.g. [2, 0]
					scores = scores[0].split('-')
					score_team_1 = scores[0]
					score_team_2 = scores[1]

					# Get the text from the stadium attribute
					stadium = stadiums[i].text

					# remove the newlines and trailing spaces and separate the name of the stadium
					#	and the name of the city by comma
					stadium = stadium.replace('\n', '')
					stadium = stadium.strip()
					stadium = stadium.split(',')
					stadium[1] = stadium[1].strip()

					stadium_name = stadium[0]
					city = stadium[1]

					
					counter += 1

					result_dict['home goals'] = score_team_1
					result_dict['away goals'] = score_team_2
					result_dict['stadium name'] = stadium_name
					result_dict['city'] = city

					results_list_of_dicts.append(result_dict)
					
					# call results_retrieve_2 to get the match details, such as scorers and assists, 
					#	red cards, penalty scorers, own goals, etc.
					team_names, player_stats, match_date, line_ups, team_stats = results_retrieve_2(driver, div_ids[i])

					print(team_names[0] + " " + score_team_1 + "-" + score_team_2 + " " + team_names[1] + " @ " + str(stadium_name) + ", " + str(city))
					
					result_dict['home'] = team_names[0]
					result_dict['away'] = team_names[1]

					results_list_of_dicts.append(match_date)
					results_list_of_dicts.append(player_stats)
					results_list_of_dicts.append(line_ups)
					results_list_of_dicts.append(team_stats)

					

					print('*****************************************************************')
					print('*****************************************************************')
					# results_list_of_dicts's elements are:
					#	[0] = basic match info (match_id, sides, goals, stadium)
					#	[1] = date information, including matchweek, and referee
					#	[2] = player events, including goal scorers with times,
					#			red cards, penalty, own goal info.
					# 	[3] = line_ups and player performances
					#	[4] = club performances
					for dict_ in results_list_of_dicts:
						print(dict_)
						print('--------------------------------------------')

					print('*****************************************************************')
					print('*****************************************************************')

					results_list_of_list_of_dicts.append(results_list_of_dicts)
					results_list_of_dicts = []

					# if there was a duplicate, start from the first result since
					#		the scraper duplicates random results, and continuing
					#		after duplication would cause the script to skip other
					#		results
					if duplicate_result_flag == True:
						i = 0
					else:
						i += 1

			return results_list_of_list_of_dicts

		except RuntimeError as runtime_error:
			print(runtime_error)

# retrieve the scorer names, and statistics after clicking on the result row
# @returns 
#	the full names of home and away sides (the previous page has the short
#		names of teams, such as 'Newcastle for Newcastle United, etc.')
#		We need the full names so that the database can recognize them
#	the name of the goal scorers, assists ...
#	the dictionaries returned by results_retrieve_3/4, so that
#	results_retrieve_1 can access them
def results_retrieve_2(driver, result_row):
	# click on the result row to open the details of the match
	driver.execute_script("arguments[0].click();", result_row)
	stats = {}

	print('###########################################################')

	# Get the full name of the teams:
	home_club_name = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='teamsContainer']/div[@class='team home']/a[@class='teamName']/span[@class='long']"))
	)

	home_club_name = home_club_name[0].text

	away_club_name = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='teamsContainer']/div[@class='team away']/a[@class='teamName']/span[@class='long']"))
	)

	away_club_name = away_club_name[0].text

	club_names = []
	club_names.append(home_club_name)
	club_names.append(away_club_name)

	print('###########################################################')
	
	# !!! have a function that handles these try-catch blocks
	try:
		# retrieve the events of the home side, which include goals (by penalty), 
		#	own goals, and red cards
		events_home_xpath = "//div[@class='matchEvents matchEventsContainer']/div[@class='home']/div[@class='event']"

		stats = extract_event(driver, events_home_xpath, stats, True)

	except TimeoutException as ex:
		print('')
	

	try:
		# retrieve the events of the away side, which include goals (by penalty), 
		#	own goals, and red cards
		events_away_xpath = "//div[@class='matchEvents matchEventsContainer']/div[@class='away']/div[@class='event']"
		
		stats = extract_event(driver, events_away_xpath, stats, False)

	except TimeoutException as ex:
		print('')

	try:
		# retrieve the assists of the home side
		assists_home_xpath = "//div[@class='assists']/div[@class='matchAssistsContainer']/div[@class='home']/div[@class='event']"
		
		stats = extract_event(driver, assists_home_xpath, stats, True)

	except TimeoutException as ex:
		print('')


	try:
		# retrieve the assists of the away side
		assists_away_xpath = "//div[@class='assists']/div[@class='matchAssistsContainer']/div[@class='away']/div[@class='event']"

		stats = extract_event(driver, assists_away_xpath, stats, False)
		print(stats)

	except TimeoutException as ex:
		print('')

	
	# print('*****************************************************************')



	match_date = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='matchDate renderMatchDateContainer']"))
	)

	match_date = match_date[0].text

	match_date_list = match_date.split()

	weekday = match_date_list[0]
	if weekday == 'Mon':
		weekday = 'Monday'
	elif weekday == 'Tuesday':
		weekday = 'Tuesday'
	elif weekday == 'Wednesday':
		weekday = 'Wednesday'
	elif weekday == 'Thursday':
		weekday = 'Thursday'
	elif weekday == 'Friday':
		weekday = 'Friday'
	elif weekday == 'Saturday':
		weekday = 'Saturday'
	elif weekday == 'Sunday':
		weekday = 'Sunday'
	day = match_date_list[1]
	month = match_date_list[2]
	year = match_date_list[3]

	match_date = {}
	match_date['weekday'] = weekday
	match_date['day'] = day
	match_date['month'] = month
	match_date['year'] = year



	# header[@class='mcHeader']/div[@class='dropDown']/
	matchweek = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//main[@id='mainContent']/div[@class='matchCentre']/header[@class='mcHeader']/div[@class='dropDown']/div[@class='current']/div[@class='long']"))
	)

	matchweek_list = matchweek[0].text.split()
	matchweek = matchweek_list[1]

	match_date['matchweek'] = matchweek

	match_referee = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='referee']"))
	)

	match_referee = match_referee[0].text
	match_date['referee'] = match_referee

	# call the retrive_3 function to get the line_ups and player stats of the match
	line_ups = results_retrieve_3(driver)
	# print(line_ups)

	# print('*****************************************************************')

	# call results_retrieve_3 function to get the team stats of the match
	team_stats = results_retrieve_4(driver)
	# print(team_stats)
	# print('*****************************************************************')	
	

	# go back to the previous page
	driver.execute_script("window.history.go(-1)")

	return club_names, stats, match_date, line_ups, team_stats
	
# get the line-ups, substitutes and player stats
def results_retrieve_3(driver):
	# get the line-ups tab on the screen
	line_ups_tab = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//li[@class='matchCentreSquadLabelContainer']"))
	)

	# click on the line-ups botton
	driver.execute_script("arguments[0].click();", line_ups_tab[0])

	# get the formation of the home team
	formation_home = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='teamList mcLineUpContainter homeLineup active']/div[@class='col-4-m ']/header[@class='squadHeader']/div[@class='position']/strong[@class='matchTeamFormation']"))
	)
	formation_home = formation_home[0].text

	# get the formation of the away team
	formation_away = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='teamList mcLineUpContainter awayLineup']/div[@class='col-4-m right']/header[@class='squadHeader']/div[@class='position']/strong[@class='matchTeamFormation']"))
	)

	formation_away = formation_away[0].text

	# get the squads of the hosts and the guests (shirt numbers and player info)
	squad_home_number = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='teamList mcLineUpContainter homeLineup active']/div[@class='col-4-m ']/div[@class='matchLineupTeamContainer']/ul[@class='startingLineUpContainer squadList home']/li[@class='player']/a/div[@class='number']"))
	)

	squad_home_info = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='teamList mcLineUpContainter homeLineup active']/div[@class='col-4-m ']/div[@class='matchLineupTeamContainer']/ul[@class='startingLineUpContainer squadList home']/li[@class='player']/a/div[@class='info']"))
	)

	squad_away_number = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='teamList mcLineUpContainter awayLineup']/div[@class='col-4-m right']/div[@class='matchLineupTeamContainer']/ul[@class='startingLineUpContainer squadList']/li[@class='player']/a/div[@class='number']"))
	)

	squad_away_info = WebDriverWait(driver, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='teamList mcLineUpContainter awayLineup']/div[@class='col-4-m right']/div[@class='matchLineupTeamContainer']/ul[@class='startingLineUpContainer squadList']/li[@class='player']/a/div[@class='info']"))
	)

	print(formation_home + ' : ' + formation_away)

	line_ups_home = extract_player_information(squad_home_number, squad_home_info, True)
	line_ups_away = extract_player_information(squad_away_number, squad_away_info, False)

	# extend the line_ups home with the line_ups_away to get both teams' line-ups of the match
	line_ups_home.update(line_ups_away)

	return line_ups_home

# get the team stats
def results_retrieve_4(driver):
	# put the entire function into try-catch block with TimeoutException as the
	#		older matches have no stats section
	try:
		# get the stats tab on the screen
		stats_tab = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "//div[@class='centralContent']/div[@class='mcTabsContainer']/div[@class='wrapper col-12']/div[@class='tabLinks matchNav']/div[@class='tabs']/ul[@class='tablist']/li[@data-tab-index='2']"))
		)
		# click on the stats botton
		driver.execute_script("arguments[0].click();", stats_tab)

		# get the stats table on the screen
		teams_stats = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='mcStatsTab statsSection season-so-far wrapper col-12 active']/table/tbody[@class='matchCentreStatsContainer']/tr"))
		)

		# append the statistics into a list
		stats_list = []

		# The format of the stats is:
		# 28.8 Possession % 71.2
		# 3 Shots on target 7
		# 		 ....
		# 11 Fouls conceded 12
		for team_stats in teams_stats:
			stats_list.append(team_stats.text)
		

		stats_dict = {}

		
		# convert the stats_list into a dictionary, where the keys are the types of
		#	the statistic along with home/away, and the values are the numbers
		#	e.g. {... 'Shots on target home': '3', 'Shots on target away': '7'}
		for i in range(0, len(stats_list)):
			first_space = stats_list[i].index(' ')
			if i == 0:
				percent_sign = stats_list[i].rindex('%')	
				type_of_stat = stats_list[i][first_space+1:percent_sign - 1]
			else:
				last_space = stats_list[i].rindex(' ')
				type_of_stat = stats_list[i][first_space + 1:last_space]

			stats_splitted = stats_list[i].split()
			stats_dict[type_of_stat + ' home'] = stats_splitted[0]
			stats_dict[type_of_stat + ' away'] = stats_splitted[len(stats_splitted) - 1]
	except TimeoutException:
		print('The match has no stats info.')
		stats_dict = {}

	return stats_dict

# Helper function for results_retrieve_3()	
# take in the rows of the squad, squad_number for the player's shirt number,
#	squad_info for the player's information in the match
# organize the data into a dictionary and return it
def extract_player_information(squad_number, squad_info, is_home_side):
	squad_dict = {}

	starting_11_counter = 1
	
	# extract the player performance (such as substition on/off, yellow/red cards, etc)
	#	from the line-ups table on the screen
	for number, info in zip(squad_number, squad_info):
		# Make a list out of the data by splitting the newlines that divide 
		#	the information
		number = number.text.splitlines()
		info = info.text.splitlines()
		
		player_info_dict = {}
		
		# recreate the temporary dictionary to store another players information
		temp_dict = {}

		temp_dict['Is Home Side'] = is_home_side
		
		# get the player's number
		player_number = number[1]
		temp_dict['Shirt Number'] = player_number
		
		# get the player's name from the list
		player_name = info[0]

		# Fill in the dictionary to be added to squad_home_dict
		if starting_11_counter <= 11:
			temp_dict['Starting 11'] = True
		else:
			temp_dict['Starting 11'] = False

		for k in range(1, len(info)):
			# when there is an element with a 'substitution on/off', then the next
			#	element has the minute at which the substition took place
			if info[k] == 'Substitution On':
				temp_dict['Substitution On'] = info[k + 1]
			elif info[k] == 'Substitution Off':
				temp_dict['Substitution Off'] = info[k + 1]
			elif info[k] == 'Yellow Card':
				temp_dict['Yellow Card'] = True
			elif info[k] == 'Red Card':
				temp_dict['Red Card'] = True
			elif info[k] == 'Pen. Scored':
				temp_dict['Pen. Scored'] = True

		# set the fields not present for the player to null later to be added to
		#	the database
		if 'Substitution On' not in temp_dict:
			temp_dict['Substitution On'] = 'Null'
		if 'Substitution Off' not in temp_dict:
			temp_dict['Substitution Off'] = 'Null'
		if 'Yellow Card' not in temp_dict:
			temp_dict['Yellow Card'] = 'Null'
		if 'Red Card' not in temp_dict:
			temp_dict['Red Card'] = 'Null'
		if 'Pen. Scored' not in temp_dict:
			temp_dict['Pen. Scored'] = 'Null' 

		squad_dict[player_name] = temp_dict

		starting_11_counter += 1

	return(squad_dict)


# Check whether the row with the given id has already been appeared on the page
def is_row_new(list_of_ids, id):
	try:
		print(id)
		x = list_of_ids.index(id)
		return False
	except ValueError:
		return True


# Find the space preceding the first digit (minute) in the string so that we can truncate 
#	the name of the goal scorer from the string that contains the name of the scorer and
#	the minute in which the goal was scored
# Returns the index of the space after the name of the player
def process_events_data(string_array, is_home):
	# string_array[0] is the player name and the time of the event
	#	which can also include (pen), (og)
	# string_array[1] is the type of the event, such as Goal, Own Goal, 
	#	label.penalty.scored
	player_name_and_time = string_array[0]
	is_assist = True

	# The assist section does not have a second line
	if len(string_array) == 2:
		is_assist = False
		event_type = string_array[1]
	else:
		event_type = 'Assist'

	if is_home == True:
		is_home = 'home'
	else:
		is_home = 'away'

	length_of_string = len(player_name_and_time)

	stats = {}

	min_array = []

	# Return a dictionary of goal scorers and assists
	# 	the first element of the array determines home or away
	#   the second element is the type of the event the followinig minutes represent
	#	e.g. stats = {'Frank Lampard': ['home', 'goal', '53', '67', '90 +6']}
	#   e.g. stats = {'Ryan Giggs': ['away', 'red card', '45 +2']}
	for char_index in range(0, length_of_string):
		if(player_name_and_time[char_index].isdigit() == True):
			scorer_name = player_name_and_time[:char_index]
			scorer_name = scorer_name.strip()
			minutes = player_name_and_time[char_index:]
			minutes = minutes.split(',')
			
			if event_type == 'Goal':
				min_array = [is_home, 'goal']
			elif event_type == 'Own Goal':
				min_array = [is_home, 'own goal']
			elif event_type == 'label.penalty.scored':
				min_array = [is_home, 'goal penalty']
			elif event_type == 'Red Card':
				min_array = [is_home, 'red card']
			elif event_type == 'Second Yellow Card (Red Card)':
				min_array = [is_home, 'Second Yellow Card (Red Card)']
			elif event_type == 'Assist':
				min_array = [is_home, 'assist']


	
			for minute in minutes:
				minute = minute.replace('\'', '')
				# Remove the (og), (pen)
				own_goal = '(og)'
				pen = '(pen)'
				if own_goal in minute:
					minute = minute.replace(own_goal, '')
				elif pen in minute:
					minute = minute.replace(pen, '')

				minute = minute.strip()
				min_array.append(minute)
				
			stats[scorer_name] = min_array

			return stats

# Extracts the event (goal, penalty, assist, etc) for a player and appends it to
#	a dictionary containing similar data.
# @parameters:
#		driver: WebDriver - to scrape the event data from the page
#		xpath: string - of the event data on the page
#		stats: dictionary - the existing event dictionary to which we add the new array of event
#			with the key being the player name
#		is_home: Boolean - is the player for the home or away side. Added to the
#			array of event data
def extract_event(driver, xpath, stats, is_home):
	try:
		# retrieve the events of the home side, which include goals (by penalty), 
		#	own goals, and red cards
		events = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, xpath))
		)
		for event in events:
			event = event.text.splitlines()

			processed_events_data_dict = process_events_data(event, is_home)
			
			# check whether the player name is already in the dictionary.
			# When the player name is already a key in the dict, e.g. if 
			#	the player has scored a goal, then trying to add an assist
			#	by the same player fails because the key already exists.
			# If the player name is already in the dictionary stats, 
			#	then append the performance array to the array
			#	already in the dictionary corresponding to the player name key,
			#   instead of adding the player name key to the dict.
			player_name = list(processed_events_data_dict.keys())[0]

			# If the player is already in the dictionary for another type of event,
			#		append the current event array to the existing array of arrays
			if player_name in stats.keys():
				stats[player_name].append(processed_events_data_dict[player_name])
			# If the player has no event data yet, create a temporary array and
			#	append the current event array to it, making an array of arrays,
			#	then adding to the dictionary with the key being the player's name.
			else:
				temp_array = []
				temp_dict = {}
				temp_array.append(processed_events_data_dict[player_name])
				temp_dict[player_name] = temp_array
				stats.update(temp_dict)

		return stats

	except TimeoutException as ex:
		# If an event is not found, still return the original stats dictionary
		#		as the following statements in the calling funciton rely on it.
		return stats

# results_retrieve_1([])