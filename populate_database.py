from premier_league_to_database import *
from premier_league_club_scraper import *
from premier_league_manager_scraper import *
from premier_league_player_scraper import *
from premier_league_results_scraper import *

# initialize the connection
connection = connect_to_database()

# initialize a database object
db = database(connection)
# db.delete_all_rows('stadium')

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


def populate_player_table():
	# # using the player_retrive_1 function to scrape player rows, filtering based on
	# #			season only
	# for j in range(0, 30):
	# 	# retrieve all the rows from player_clubs table corresponding to the given season
	# 	season = all_seasons[j]
	# 	print(season)
	# 	player_club_list_of_dicts = db.get_player_clubs(season)
		
	# 	# for dict_ in player_club_list_of_dicts:
	# 	#  	print(dict_)
	
	# 	player_list_of_dicts = player_retrieve_1(player_club_list_of_dicts, j)
		
	# 	for player_dict in player_list_of_dicts:
	# 		db.insert_players(player_dict)

	# using the player_retrieve_by_season_and_club function to filter based on
	#			season and club
	
	# Iterate over the seasons, and after a season's data is scraped, insert that data
	#		into the database, and move on to the next iteration.
	# !!! do j = 4 again (1996/97)
	for j in range(0, 5):
		season = all_seasons[j]
		player_club_list_of_dicts = db.get_player_clubs(season)

		player_list_of_dicts = player_retrieve_by_season_and_club(player_club_list_of_dicts, j)
		
		for player_dict in player_list_of_dicts:
			db.insert_players(player_dicst)

	# close the connection
	connection.close()


def populate_match_table():
	# iterate over the seasons and get their results
	for j in range(9, 10):
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

				# update the stadiums_and_cities_dict
				db.insert_match_basic_info(match_info_list_of_dicts[0], match_info_list_of_dicts[1])

				match_id_and_club_names = []
				match_id_and_club_names.append(match_info_list_of_dicts[0]['match id'])
				match_id_and_club_names.append(match_info_list_of_dicts[0]['home'])
				match_id_and_club_names.append(match_info_list_of_dicts[0]['away'])
				match_id_and_club_names.append(match_info_list_of_dicts[0]['season'])


				db.insert_player_performance(match_info_list_of_dicts[2], match_id_and_club_names[0])
				db.insert_player_stats(match_info_list_of_dicts[3], match_id_and_club_names[0])
				db.insert_club_stats(match_info_list_of_dicts[4], match_id_and_club_names)
			except IntegrityError:
				print('Duplicate Key error raised from the insert_match_basic_info.')

# populate_stadium_and_club_tables()
# populate_manager_table()
# populate_player_table()
# populate_match_table
for j in range(1, 5):
	players_dict = player_duplicate_check(j)

	for player_id, player_name in players_dict.items():
		db.insert_into_duplicate_players(player_id, player_name)
# # db.generate_standings()