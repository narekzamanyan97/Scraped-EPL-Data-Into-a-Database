from premier_league_to_database import *
from premier_league_club_scraper import *
from premier_league_manager_scraper import *
from premier_league_player_scraper import *
from premier_league_results_scraper import *
from premier_league_fixtures_scraper import *
from fast_match_scraper import *

# initialize the connection
connection = connect_to_database()

# initialize a database object
db = database(connection)

# gets club and stadium data using the scraper functions and inserts them into the club and stadium tables
def populate_stadium_and_club_tables():
	# call the club_retrieve_1() function, that returns a list of dictionaries
	#	of 20 clubs, to get the club data
	club_list_of_dicts = club_retrieve_1()

	# iterate through the list to work with the individual club dictionaries
	#	that contain club and stadium information
	for club_dict in club_list_of_dicts:
		print(club_dict)
		db.insert_stadiums(club_dict)
		db.insert_clubs(club_dict)
	
	# close the connection
	connection.close()

# gets manager data using the scraper functions and inserts them into the manager table
def populate_manager_table():
	all_managers_list_of_dicts = all_seasons_manager_retrieve()

	for all_managers_dict in all_managers_list_of_dicts:
		db.insert_managers(all_managers_dict)
	
	managers_list_of_dicts = manager_retrieve_1()

	for managers_dict in managers_list_of_dicts:
		manager_name = managers_dict['manager name']
		club_name = managers_dict['manager club']
		season = managers_dict['season']

		db.insert_manager_club(manager_name, club_name, season)


	# close the connection
	connection.close()

# gets player data using the scraper functions and inserts them into the player table
def populate_player_table():
	# using the player_retrive_1 function to scrape player rows, filtering based on
	#			season only
	for j in range(8, 9):
		# retrieve all the rows from player_clubs table corresponding to the given season
		season = all_seasons[j]
		print(season)
		player_club_list_of_dicts = db.get_player_clubs(season)
		

		# # scrape the player info
		# player_list_of_dicts = player_retrieve_by_season_and_club(player_club_list_of_dicts, j)
		# player_dict_of_lists = player_retrieve_1(player_club_list_of_dicts, j)

		# # iterate over the scraped list of dictionaries of players and insert
		# # 	each item into the database
		# for player_dict in player_list_of_dicts:
		# 	db.insert_players(player_dict)

		# *****************************************************************************
		# # get the correct country and position names for each player
		# # call the new function to get the correct country and position info
		# player_dict_of_lists = player_get_the_correct_country_and_position(j)
		# # Updating (fixing) the country and position of players
		# for player_id, country_and_position in player_dict_of_lists.items():
		# 	# print(player_id + '--------' + str(country_and_position))
		# 	country = country_and_position[0]
		# 	position = country_and_position[1]

		# 	db.update_player_country_and_club(player_id, country, position)
		# *****************************************************************************


	# using the player_retrieve_by_season_and_club function to filter based on
	#			season and club

	# Iterate over the seasons, and after a season's data is scraped, insert that data
	#		into the database, and move on to the next iteration.
	# !!! do j = 4 again (1996/97) does not work
	for j in range(5, len(all_seasons)):
		season = all_seasons[j]
		player_club_list_of_dicts = db.get_player_clubs(season)

		player_list_of_dicts = player_retrieve_by_season_and_club(player_club_list_of_dicts, j)
		
		for player_dict in player_list_of_dicts:
			db.insert_players(player_dict)

	# close the connection
	connection.close()

def update_img_url_for_players():
	# get the list of all players
	list_of_player_ids = db.get_list_of_all_player_ids()
	# generate the image urls for each player
	generated_urls = player_generate_img_url(list_of_player_ids)

	db.insert_player_img_urls(generated_urls)

def update_badge_url_for_clubs():

	# get the dictionary of club badges
	dict_of_badges = club_badge_retrieve()

	# print(dict_of_badges)

	for club_name, url_list in dict_of_badges.items():
		badge_url = url_list[0]
		stadium_img_url = url_list[1]

		print(club_name)
		print(badge_url)
		print(stadium_img_url)
		
		db.insert_club_badge_and_stadium(club_name, badge_url, stadium_img_url)
		print('-----------------------------')


# gets match data using the scraper functions and inserts them into the match_, club_stats, player_stats,
#		and player_performance tables
def populate_match_table():
	# iterate over the seasons and get their results
	for j in range(18, 19):
		all_match_ids_in_db = db.get_all_match_ids_inserted()

		all_stadiums_and_cities_list_of_dicts = db.get_stadiums()
	
		print(all_stadiums_and_cities_list_of_dicts)

		match_info_list_of_list_of_dicts = results_retrieve_1(all_match_ids_in_db, j)

		for match_info_list_of_dicts in match_info_list_of_list_of_dicts:
			try:
				print('*********************************************************')
				for stadium_name, city in match_info_list_of_dicts[5].items():
					print('stadium_name = ' + stadium_name)
					print('city = ' + city)

					stadium_was_found = False
					# iterate through the stadium_city list of dictionaries
					for stadium_city_dict in all_stadiums_and_cities_list_of_dicts:

						# if the dictionary is of the given stadium
						if stadium_city_dict['stadium_name'] == stadium_name:

							stadium_was_found = True
							print('stadium_city_dict: ' + str(stadium_city_dict))

							# if the city is null, then call the update_stadium_city function
							if stadium_city_dict['city'] == None:
								print('Updating the city of the stadium.')
								db.update_stadium_city(match_info_list_of_dicts[5])
							else:
								print('The stadium already has the city info.')
				
					# the stadium was not found, so add it to the stadium table, using
					#		the stadium_name and city
					if stadium_was_found == False:
						print('inserting the old stadium.')
						db.insert_old_stadium(stadium_name, city)

				db.insert_match_basic_info(match_info_list_of_dicts[0], match_info_list_of_dicts[1])

				match_id_and_club_names = []
				match_id_and_club_names.append(match_info_list_of_dicts[0]['match id'])
				match_id_and_club_names.append(match_info_list_of_dicts[0]['home'])
				match_id_and_club_names.append(match_info_list_of_dicts[0]['away'])
				match_id_and_club_names.append(match_info_list_of_dicts[0]['season'])


				db.insert_player_performance(match_info_list_of_dicts[2], match_id_and_club_names[0])
				print(match_info_list_of_dicts[3])
				db.insert_player_stats(match_info_list_of_dicts[3], match_id_and_club_names[0])
				db.insert_club_stats(match_info_list_of_dicts[4], match_id_and_club_names)
			except IntegrityError:
				print('Duplicate Key error raised from the insert_match_basic_info.')

# gets match data using the scraper functions and inserts them into the match_, club_stats, player_stats,
#		and player_performance tables
def fast_populate_match_table():


	matches = db.get_match_ids_with_pen_goals()
	
	
	match_info_list_of_list_of_dicts = fast_results_retrieve([7333])

	for match_info_list_of_dicts in match_info_list_of_list_of_dicts:
		try:
			db.insert_match_basic_info(match_info_list_of_dicts[0], match_info_list_of_dicts[1])

			match_id_and_club_names = []
			match_id_and_club_names.append(match_info_list_of_dicts[0]['match id'])
			match_id_and_club_names.append(match_info_list_of_dicts[0]['home'])
			match_id_and_club_names.append(match_info_list_of_dicts[0]['away'])
			match_id_and_club_names.append(match_info_list_of_dicts[0]['season'])


			db.insert_player_performance(match_info_list_of_dicts[2], match_id_and_club_names[0])
			print(match_info_list_of_dicts[3])
			db.insert_player_stats(match_info_list_of_dicts[3], match_id_and_club_names[0])
			db.insert_club_stats(match_info_list_of_dicts[4], match_id_and_club_names)
		except IntegrityError:
			print('Duplicate Key error raised from the insert_match_basic_info.')



def populate_fixture_table():
	fixtures_dict_of_dicts = fixtures_retrieve()

	for fixture_id, fixture_dict in fixtures_dict_of_dicts.items():
		print(fixture_id)
		print(fixture_dict)

		db.insert_fixtures(fixture_id, fixture_dict)

		print('---------------------------------------------------')

# populate_stadium_and_club_tables()
# populate_manager_table()
# populate_player_table()
# update_img_url_for_players()
# update_badge_url_for_clubs()
# populate_match_table()
fast_populate_match_table()
# populate_fixture_table()

# for j in range(1, 5):
# 	players_dict = player_duplicate_check(j)

# 	for player_id, player_name in players_dict.items():
# 		db.insert_into_duplicate_players(player_id, player_name)


# for season_index in range(20, len(all_seasons)):
# 	managers_list_of_dicts = manager_duplicate_check(season_index)

# 	for managers_dict in managers_list_of_dicts:
# 		db.insert_into_duplicate_managers(managers_dict['manager_id'], managers_dict['manager name'])

# # db.generate_standings()