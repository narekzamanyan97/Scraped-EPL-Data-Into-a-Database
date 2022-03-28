from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import time
import re

import json

from set_up_driver import *

from helper_functions import *
from premier_league_results_scraper import *

from premier_league_to_database import *

urls = {
	'url_1': 'https://www.premierleague.com/match/',
}

def yellow_card_detail_scraper(list_of_all_match_ids):
	driver = set_up_driver(urls['url_1'])


	# store the yellow_card details (i.e. minute, match_id, player_id) in this dictionary
	# e.g. {'22222': [{'minute': 32, 'player_id': 'p22'}, {'minute': 34, 'player_id': 'p222'}],
	#		'22223': [{'minute': 2, 'player_id': 'p2'}, {'minute': 33, 'player_id': 'p2322'}]}
	yellow_card_dict_of_lists = {}

	attendance_dict = {}

	# for i in list_of_all_match_ids:
	for i in range(7333, 7334):
		driver.get(urls['url_1'] + str(i))


		match_id = i

		# ==================== Scrape Attendance ====================
		# get attendance of the match
		attendance = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='attendance hide-m']"))
		)

		# remove the Att from the string
		attendance = attendance[0].text.replace('Att: ', '')

		attendance_dict[match_id] = attendance
		print(attendance)


		# ==================== Scrape Yellow Cards ====================
		# get the minutes on the timeline
		timeline_minutes = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='eventLine timeLineEventsContainer']/div/div[@class='eventInfoContainer ']/div[@class='eventInfo']/header[@class='eventInfoHeader']/time[@class='min']"))
		)

		# get the type of the event (e.g. goal, yellow_card, red_card, etc.)
		timeline_event_type = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='eventLine timeLineEventsContainer']/div/div[@class='eventInfoContainer ']/div[@class='eventInfo']/header[@class='eventInfoHeader']/span[@class='visuallyHidden']"))
		)

		# get the player associated with the event (for sub, 2 players are associated with the event.)
		#		Here, we only care about yellow cards received by a player
		timeline_player = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='eventLine timeLineEventsContainer']/div/div[@class='eventInfoContainer ']/div[@class='eventInfo']/div[@class='eventInfoContent ']/img"))
		)


	
		# this list will contain dictionaries of yellow card details that belong to the same match:
		#	e.g. [{'minute': 32, 'player_id': 'p22'}, {'minute': 34, 'player_id': 'p222'}]
		temp_list_of_dicts = []
		
		for index in range(0, len(timeline_minutes)):
			event_type = timeline_event_type[index].get_attribute('textContent')
			
			if event_type == 'Yellow Card':
				temp_dict = {}
			
				event_minute = timeline_minutes[index].get_attribute('textContent')
				player_id = timeline_player[index].get_attribute('data-player')
				
				temp_dict['minute'] = event_minute
				temp_dict['player_id'] = player_id
				temp_list_of_dicts.append(temp_dict)

				# print(event_minute, end='---')
				# print(event_type, end='---')
				# print(player_id)
		print(str(match_id) + ': ' + str(temp_list_of_dicts))
		yellow_card_dict_of_lists[match_id] = temp_list_of_dicts




		# ==================== Scrape Scores ====================
		# this query gets all the match ids and number of penalties where
		#		the number of penalties is more than the actual value.
		# select match_id, count(*) as penalties from player_performance where type_of_stat=2 group by match_id having penalties>1 order by match_id;

	# for match_id, yellow_card_list in yellow_card_dict_of_lists.items():
	# 	print(str(match_id) + ': ' + str(yellow_card_list))
	print(attendance_dict)
	return attendance_dict, yellow_card_dict_of_lists


# !!! Use the match_ids (rather than clicking on match rows, then going back, and wasting a lot of time)
#	in the url to retrieve the team names, score, the stadium name, and its city
# 	@parameters:
#	the list of match_ids to be scraped
#	list_of_all_match_ids_and_seasons = [{'match_id': 22222, 'season': '2001/2002'}, {'match_id': 2222, 'season': '1995/1996'}, ... ]
def fast_results_retrieve(list_of_all_match_ids_and_seasons):
	driver = set_up_driver(urls['url_1'])

	# holds all the results
	results_list_of_dicts = []
	results_list_of_list_of_dicts = []

	# iterate over the clubs
	for match_id_and_season_dict in list_of_all_match_ids_and_seasons:
		match_id = match_id_and_season_dict['match_id']
		season = match_id_and_season_dict['season']

		driver.get(urls['url_1'] + str(match_id))



		time.sleep(2.22)
		# exit accept all cookies prompt by accepting it
		try:
			advert_xpath = "//button[@class='_2hTJ5th4dIYlveipSEMYHH BfdVlAo_cgSVjDUegen0F js-accept-all-close']"
			advert = presence_of_all_el_located(driver, advert_xpath, SECONDS_TO_WAIT, -2)
			ad_close_button = advert[0]

			# click on the close button
			driver.execute_script("arguments[0].click();", ad_close_button)
			print('clicked on close button')
		
		except TimeoutException:
			print('There is no advertisement button. Moving on!')


		print('***************************************************************************************************')

		# holds a result information
		result_dict = {}
		result_dict['match id'] = match_id

		# add the season to the result_dict
		result_dict['season'] = season


		scoreline = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='teamsContainer']"))
		)
		print('scoreline.text')
		print(scoreline[0].text)

		# truncated is an array of strings with the following format:
		# ['team_name_1', 'team_1_goals-team_2_goals', 'team_name_2']
		# truncated = result.text.splitlines()
		truncated = scoreline[0].text.splitlines()

		# retrieve team names
		home_team_name = truncated[0]
		away_team_name = truncated[2]


		# retrieve the scores
		scoresheet = truncated[1]

		# scores is an array of 2 elements with the number of goals for each
		# 	team. e.g. ['2-0']
		scores = scoresheet.splitlines()

		# scores now is an array with the number of goals as its elements
		#	e.g. [2, 0]
		scores = scores[0].split('-')
		score_team_1 = scores[0]
		score_team_2 = scores[1]

		print(home_team_name + ' ' + score_team_1 + ' - ' + score_team_2 + ' ' + away_team_name)

		# get the stadium element
		stadium = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='matchInfo']/div[@class='stadium']"))
		)

		# Get the text from the stadium attribute
		stadium = stadium[0].text
	

		# remove the newlines and trailing spaces and separate the name of the stadium
		#	and the name of the city by comma
		stadium = stadium.replace('\n', '')
		stadium = stadium.strip()
		stadium = stadium.split(',')
		stadium[1] = stadium[1].strip()

		stadium_name = stadium[0]
		city = stadium[1]

		result_dict['home goals'] = score_team_1
		result_dict['away goals'] = score_team_2
		result_dict['stadium name'] = stadium_name
		result_dict['city'] = city

		results_list_of_dicts.append(result_dict)
		
		# get the date of the match, e.g. Tue 22 May 2022
		match_date = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='mcTabsContainer']"))
		)

		match_date_json_string = match_date[0].get_attribute('data-fixture')

		match_date_json_dict = json.loads(match_date_json_string)

		match_date_long = match_date_json_dict['kickoff']['label']

		# extract the weekday, day, month, and year from the match_date
	
		match_date = {}

		match_date_list = match_date_long.split()

		weekday = match_date_list[0]
		day = match_date_list[1]
		month = match_date_list[2]
		year = match_date_list[3].replace(',', '')
		print(weekday)
		print(day)
		print(month)
		print(year)

		match_date = {}
		match_date['weekday'] = weekday
		match_date['day'] = day
		match_date['month'] = month
		match_date['year'] = year



		# call results_retrieve_2 to get the match details, such as scorers and assists, 
		#	red cards, penalty scorers, own goals, etc.
		team_names, player_stats, match_date_, line_ups, team_stats = results_retrieve_2(driver, season)

		# if the season is 2006/07 or more recent, then results_retrieve_2 was able to retrieve the match date.
		match_date.update(match_date_)
		

		print(team_names[0] + " " + score_team_1 + "-" + score_team_2 + " " + team_names[1] + " @ " + str(stadium_name) + ", " + str(city))
		
		print('team_names[0] = ' + team_names[0])
		print('team_names[1] = ' + team_names[1])
		
		result_dict['home'] = team_names[0]
		result_dict['away'] = team_names[1]

		results_list_of_dicts.append(match_date)
		results_list_of_dicts.append(player_stats)
		results_list_of_dicts.append(line_ups)
		results_list_of_dicts.append(team_stats)
		# results_list_of_dicts.append(stadium_city_dict)

		

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


	return results_list_of_list_of_dicts


def get_match_ids_and_dates():
	# get the date of the match if season <= 2006/07. Otherwise, the date will be found in the result page
	print(all_seasons[j])
	match_date = {}
	if all_seasons[j] < '2006/07':
		result_parent = results[i].find_element_by_xpath('../../../../..')
		match_date = result_parent.get_attribute('data-competition-matches-list')

		match_date_list = match_date.split()

		weekday = match_date_list[0]
		day = match_date_list[1]
		month = match_date_list[2]
		year = match_date_list[3]

		match_date = {}
		match_date['weekday'] = weekday
		match_date['day'] = day
		match_date['month'] = month
		match_date['year'] = year

# initialize the connection
connection = connect_to_database()

# initialize a database object
db = database(connection)

list_of_all_match_ids = db.get_all_match_ids()

fast_results_retrieve([{'match_id': 7333, 'season': '2010/11'}])

attendance_dict, yellow_card_dict_of_lists = yellow_card_detail_scraper(list_of_all_match_ids)

db.update_yellow_card_minutes(yellow_card_dict_of_lists)
db.update_attendance(attendance_dict)