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
	#	that contains club and stadium information
	for club_dict in club_list_of_dicts:
		print(club_dict)
		db.insert_stadiums(club_dict)
		db.insert_clubs(club_dict)
	# close the connection
	connection.close()

def populate_manager_table():
	managers_list_of_dicts = manager_retrieve_1()

	for managers_dict in managers_list_of_dicts:
		db.insert_managers(managers_dict)
	# close the connection
	connection.close()


def populate_player_table():
	player_list_of_dicts = player_retrieve_1()
	
	for player_dict in player_list_of_dicts:
		# print(player_dict)
		db.insert_players(player_dict)

	# close the connection
	connection.close()


def populate_match_table():
	match_info_list_of_list_of_dicts = results_retrieve_1()

	for match_info_list_of_dicts in match_info_list_of_list_of_dicts:
		try:
			db.insert_match_basic_info(match_info_list_of_dicts[0], match_info_list_of_dicts[1])

			match_id_and_club_names = []
			match_id_and_club_names.append(match_info_list_of_dicts[0]['match id'])
			match_id_and_club_names.append(match_info_list_of_dicts[0]['home'])
			match_id_and_club_names.append(match_info_list_of_dicts[0]['away'])

			db.insert_player_performance(match_info_list_of_dicts[2], match_id_and_club_names[0])
			db.insert_player_stats(match_info_list_of_dicts[3], match_id_and_club_names[0])
			db.insert_club_stats(match_info_list_of_dicts[4], match_id_and_club_names)
		except IntegrityError:
			print('Duplicate Key error raised from the insert_match_basic_info.')




# populate_stadium_and_club_tables()
# populate_manager_table()
# populate_player_table()
populate_match_table()