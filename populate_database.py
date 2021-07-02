from premier_league_to_database import *

from premier_league_club_scraper import *

from premier_league_manager_scraper import *


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
	print(managers_list_of_dicts)
	for managers_dict in managers_list_of_dicts:
		db.insert_managers(managers_dict)



populate_manager_table()


# populate_stadium_and_club_tables()