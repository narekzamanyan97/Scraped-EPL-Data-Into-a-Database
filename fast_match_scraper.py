from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import time
import re

from set_up_driver import *

from helper_functions import *

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

	for i in list_of_all_match_ids:
		driver.get(urls['url_1'] + str(i))


		match_id = i

		# get attendance of the match
		attendance = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//div[@class='attendance hide-m']"))
		)

		attendance = attendance[0].text

		attendance_dict[match_id] = attendance
		print(attendance)

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

	# for match_id, yellow_card_list in yellow_card_dict_of_lists.items():
	# 	print(str(match_id) + ': ' + str(yellow_card_list))
	return attendance_dict, yellow_card_dict_of_lists

# initialize the connection
connection = connect_to_database()

# initialize a database object
db = database(connection)

list_of_all_match_ids = db.get_all_match_ids()

yellow_card_detail_scraper(list_of_all_match_ids)