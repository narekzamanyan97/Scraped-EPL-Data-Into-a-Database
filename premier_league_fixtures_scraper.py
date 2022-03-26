from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import time
import re

from set_up_driver import *

from helper_functions import *

urls = {
	'url_1': 'https://www.premierleague.com/fixtures',
}

SECONDS_TO_WAIT = 5

# retrieve the team names, score, the stadium name, and its city
# 	Argument:
#		list of all the match_ids available in the table. This is to save time
#		and skip over the match_ids that have already been considered before
def fixtures_retrieve():
	driver = set_up_driver(urls['url_1'])
	
	fixtures_dict_of_dicts = {}

	# iterate over the clubs
	for club_index in range(10, 12):
		# filter using the next club
		filter_club = WebDriverWait(driver, 15).until(
			EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='dropdownList' and @data-dropdown-list='teams']/li[@role='option' and @data-option-index=\"" + str(club_index) + "\"]"))
		)
		
		# choose the next club from the season
		driver.execute_script("arguments[0].click();", filter_club[0])
		time.sleep(5)

		# Scroll down to load more results to include all the results
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(5)


		# get access to the fixture dates and fixtures. Both lists will have the
		#		same amount of rows because each match is played in a single date
		fixture_dates = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//section[@class='fixtures']/time[@class='date long']/strong"))
		)

		fixtures = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//section[@class='fixtures']/div[@class='fixtures__matches-list']/ul[@class='matchList']/li[@class='matchFixtureContainer']/div[@class='fixture preMatch']/span[@class='overview']"))
		)

		fixture_ids = WebDriverWait(driver, 10).until(
			EC.presence_of_all_elements_located((By.XPATH, "//section[@class='fixtures']/div[@class='fixtures__matches-list']/ul[@class='matchList']/li[@class='matchFixtureContainer']/div[@class='fixture preMatch']"))
		)


		for i in range(0, len(fixture_dates)):
			temp_fixture_details_dict = {}


			# get the fixtrue id
			fixture_id = fixture_ids[i].get_attribute('data-matchid')

			# if there is at most one date to be confirmed rows
			match_date = fixture_dates[i].text
			
			# if there are two date to be confirmed rows
			# if i == 0:
			# 	# get match date
			# 	match_date = fixture_dates[i].text
			# else:
			# 	# get match date
			# 	match_date = fixture_dates[i-1].text
			# if there are 3 date to be confirmed rows
			# if i <= 1:
			# 	# get match date
			# 	match_date = fixture_dates[0].text
			# else:
			# 	# get match date
			# 	match_date = fixture_dates[i-2].text

			# generate YYYY-MM-DD format for the date
			match_date_list = match_date.split(' ')
			# if the date is not "Date To Be Confirmed" extract the year, day, and month
			if match_date_list[0] != 'Date':
				weekday = match_date_list[0]
				day = match_date_list[1]
				day = append_0_to_day(day)
				month = match_date_list[2]
				month_number = month_to_number_converter(month)
				year = match_date_list[3]

				match_date_formatted = year + '-' + month_number + '-' + day
			# default date
			else:
				weekday = 'Monday'
				match_date_formatted = '2022-02-22'

			# process the fixture row to get the home and away team names,
			#		match time, and stadium info
			fixture_details = fixtures[i].text
			fixture_details_list = fixture_details.splitlines()


			home_team_name = fixture_details_list[0]
			home_team_full_name = full_name_converter(home_team_name)

			fixture_time = fixture_details_list[1]  
			if fixture_time == 'TBC':
				fixture_time = '7:00'

			# formatted_fixture_time = format_time(fixture_time.strip())

			away_team_name = fixture_details_list[2]
			away_team_full_name = full_name_converter(away_team_name)

			stadium_name = fixture_details_list[3].replace(',', '')

			print(match_date_formatted)
			print(fixture_id)
			print(match_date_list)
			print(home_team_full_name + ' - ' + fixture_time + ' - ' + away_team_full_name + ' - ' + stadium_name)


			temp_fixture_details_dict['fixture_date'] = match_date_formatted.strip()
			temp_fixture_details_dict['home_team_name'] = home_team_full_name.strip()
			temp_fixture_details_dict['away_team_name'] = away_team_full_name.strip()
			temp_fixture_details_dict['fixture_time'] = fixture_time
			temp_fixture_details_dict['stadium_name'] = stadium_name.strip()
			temp_fixture_details_dict['weekday'] = weekday.strip()



			fixtures_dict_of_dicts[fixture_id] = temp_fixture_details_dict

			# print(fixtures_dict_of_dicts)

			print('------------------------------------------------')

	return fixtures_dict_of_dicts

# takes the short name of the club (e.g. Man Utd, Wolves) and converts it
#		into its full name (Manchester United, Wolverhampton Wanderers)
def full_name_converter(club_name):
	club_full_name = ''

	if club_name == 'Wolves':
		club_full_name = 'Wolverhampton Wanderers'
	elif club_name == 'Man City':
		club_full_name = 'Manchester City'
	elif club_name == 'Man Utd':
		club_full_name = 'Manchester United'
	elif club_name == 'Brighton':
		club_full_name = 'Brighton and Hove Albion'
	elif club_name == 'West Ham':
		club_full_name = 'West Ham United'
	elif club_name == 'Leeds':
		club_full_name = 'Leeds United'
	elif club_name == 'Leicester':
		club_full_name = 'Leicester City'
	elif club_name == 'Newcastle':
		club_full_name = 'Newcastle United'
	elif club_name == 'Norwich':
		club_full_name = 'Norwich City'
	elif club_name == 'Spurs':
		club_full_name = 'Tottenham Hotspur'
	else:
		club_full_name = club_name

	return club_full_name

# convert month name (e.g. January) to its corresponding number (e.g. 01)
def month_to_number_converter(month_name):
	month_number = ''

	if month_name == 'January':
		month_number = '01'
	if month_name == 'February':
		month_number = '02'
	if month_name == 'March':
		month_number = '03'
	if month_name == 'April':
		month_number = '04'
	if month_name == 'May':
		month_number = '05'
	if month_name == 'June':
		month_number = '06'
	if month_name == 'July':
		month_number = '07'
	if month_name == 'August':
		month_number = '08'
	if month_name == 'September':
		month_number = '09'
	if month_name == 'October':
		month_number = '10'
	if month_name == 'November':
		month_number = '11'
	if month_name == 'December':
		month_number = '12'

	return month_number

def format_time(fixture_time):
	formatted_fixture_time = fixture_time + ':00'

	hour = formatted_fixture_time.partition(':')[0]

	if len(hour) == 1:
		formatted_fixture_time = '0' + formatted_fixture_time

	return formatted_fixture_time


# append 0 to a day of the date (e.g. 01 of 1, 09 for 9. Leave 10+ days the same)
def append_0_to_day(day):
	full_day = ''

	if day in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
		full_day = '0' + day
	else:
		full_day = day

	return full_day

# fixtures_retrieve()