import mysql.connector as connector
from mysql.connector import Error
from connect_to_database import *


def query(conn, query_string, change=False):
	# instantiate a cursor object to interact with MySQL server and
	#	execute queries
	cursor = conn.cursor()
	# execute the given query statement
	cursor.execute(query_string)
	# if the query changes the database, then commit the changes
	if change == True:
		conn.commit()
	else:
		# get the rows of the query result set as a list of tuples
		# 	we must fetch all rows for the current query before executing
		#	new statements using the same connection
		tuple_list = cursor.fetchall()

		# !!! convert tuplelist to dict list if necessary
		conn.close()
		return tuple_list

# Takes in a list of tuples and returns a list of dictionaries of those tuples
# def convert_tuplelist_to_dictlist(cursor, tuples):

class database:
	cursor = ''
	conn = ''

	def __init__(self, conn):
		self.conn = conn
		self.cursor = self.conn.cursor()

	# prints every row in a given tuple
	def print_table(self, table_name):
		query_string = "SELECT * "
		query_string += "FROM " + str(table_name) + ";"

		self.cursor.execute(query_string)
		tuple_list = self.cursor.fetchall()

	def insert_managers(self, managers_dict):
		insert_statement = "INSERT INTO manager(club_id, manager_name, country, active, joined_club, date_of_birth, epl_seasons, epl_debut_match) "
		
		country = managers_dict['Country of Birth']
		manager_name = managers_dict['manager name']
		status = managers_dict['Status']
		if status == 'Active':
			active = True
		else:
			active = False
		# some managers don't have 'Joined Club' date, so KeyError can 
		#	be thrown
		try:
			joined_club = managers_dict['Joined Club']
			splitted_joined_club = joined_club.split(' ')
			joined_club_day = splitted_joined_club[0]
			joined_club_month = splitted_joined_club[1]
			joined_club_year = splitted_joined_club[2]

			# convert the month name into number from 01 to 12
			if joined_club_month == "January":
				joined_club_month = '01'
			elif joined_club_month == "February":
				joined_club_month = '02'
			elif joined_club_month == 'March':
				joined_club_month = '03'
			elif joined_club_month == 'April':
				joined_club_month = '04'
			elif joined_club_month == 'May':
				joined_club_month = '05'
			elif joined_club_month == 'June':
				joined_club_month = '06'
			elif joined_club_month == 'July':
				joined_club_month = '07'
			elif joined_club_month == 'August':
				joined_club_month = '08'
			elif joined_club_month == 'September':
				joined_club_month = '09'
			elif joined_club_month == 'October':
				joined_club_month = '10'
			elif joined_club_month == 'November':
				joined_club_month = '11'
			elif joined_club_month == 'December':
				joined_club_month = '12'
			joined_club_date = joined_club_year + '-' + joined_club_month + '-' + joined_club_day
		except KeyError:
			joined_club_date = '0000-00-00'
	
		# get the date_of_birth and change the format from DD/MM/YYYY into
		#	MM-DD-YYYY 
		date_of_birth = managers_dict['Date of Birth']
		splitted_date_of_birth = date_of_birth.split('/')
		dob_day = splitted_date_of_birth[0]
		dob_month = splitted_date_of_birth[1]
		dob_year = splitted_date_of_birth[2]

		# format date of birth into mysql date type
		dob_date = dob_year + '-' + dob_month + '-' + dob_day	

		epl_seasons = managers_dict['Premier League Seasons']
		epl_debut_match = managers_dict['Premier League Debut Match']



		# !!! get the club id
		club_name = managers_dict['manager club']

		club_id_query = "SELECT club_id "
		club_id_query += "FROM club "
		club_id_query += "WHERE club_name=\"" + club_name + "\";"

		self.cursor.execute(club_id_query)
		tuple_list = self.cursor.fetchall()
		club_id = tuple_list[0][0]

		insert_statement += "VALUES(" + str(club_id) + ", "
		insert_statement += "\"" + str(manager_name) + "\", "
		insert_statement += "\"" + str(country) + "\", "
		insert_statement += str(active) + ", "
		insert_statement += "\"" + joined_club_date + "\", "
		insert_statement += "\"" + dob_date + "\", "
		insert_statement += "\"" + epl_seasons + "\", "
		insert_statement += "\"" + epl_debut_match + "\");"

		self.cursor.execute(insert_statement)
		self.conn.commit()



	def insert_players(self, player_dict):
		insert_statement = "INSERT INTO player(club_id, player_name, player_number, position, country, date_of_birth, height) "

		# !!! get the club_id

		club_name = player_dict['club']

		# some club names end with '(loan)'. If that is the case, then remove 
		#	the 'loan' substring
		if '(loan)' in club_name:
			# remove the '(loan)' from the club name
			club_name = club_name.replace('(loan)', '')
		# the 'L' in loan can be capitalized
		elif '(Loan)' in club_name:
			club_name = club_name.replace('(Loan)', '')

		# remove U21 from the club_name
		if 'U21' in club_name:
			club_name = club_name.replace('U21', '')

		# remove trailing spaces
		club_name = club_name.strip()

		# For the player Lars Dendoncker, the club name has the '&' instead of
		#	'and for Brighton and Hove Albion'
		if club_name == 'Brighton & Hove Albion':
			print('Changing the Brighton name')
			club_name = 'Brighton and Hove Albion'


		club_id_query = "SELECT club_id "
		club_id_query += "FROM club "
		club_id_query += "WHERE club_name=\"" + club_name + "\";"

		self.cursor.execute(club_id_query)
		tuple_list = self.cursor.fetchall()
		
		try:
			club_id = tuple_list[0][0]
		except IndexError:
			club_id = 'Null'

		player_name = player_dict['player name']
		position = player_dict['position']
		country = player_dict['country']
		try:
			shirt_number = player_dict['shirt number']
		except KeyError:
			shirt_number = 'Null'
		# there is (are) players without specified date of birth
		date_of_birth = player_dict['date of birth']
		if date_of_birth != '0000-00-00':				
			dob_list = date_of_birth.split('/')
			dob_day = dob_list[0]
			dob_month = dob_list[1]
			dob_year = dob_list[2]
			dob_date = dob_year + '-' + dob_month + '-' + dob_day
		else:
			dob_date = date_of_birth		

		try:
			height = player_dict['height']
			# remove the 'cm' from the height
			height_list = height.split('c')
			height = height_list[0]
		except KeyError:
			height = 'Null'

		insert_statement += "VALUES(" + str(club_id) + ", "
		insert_statement += "\"" + player_name + "\", "
		insert_statement += str(shirt_number) + ", "
		insert_statement += "\"" + position + "\", "
		insert_statement += "\"" + country + "\", "
		insert_statement += "\"" + dob_date + "\", "
		insert_statement += str(height) + ");"

		self.cursor.execute(insert_statement)
		self.conn.commit()

	# get the stadium_name to obtain stadium_id from the stadium table
	def insert_clubs(self, club_dict):
		insert_statement = "INSERT INTO club (stadium_id, club_name, website) "

		club_name = club_dict['club name']
		website = club_dict['website']

		# get the stadium id from the stadium table
		stadium_name = club_dict['stadium name']

		stadium_id_query = "SELECT stadium_id "
		stadium_id_query += "FROM stadium "
		stadium_id_query += "WHERE stadium_name=\"" + stadium_name + "\";"

		self.cursor.execute(stadium_id_query)
		tuple_list = self.cursor.fetchall()
		stadium_id = tuple_list[0][0]

		insert_statement += "VALUES(" + str(stadium_id) + ", "
		insert_statement += "\"" + str(club_name) + "\", "
		insert_statement += "\"" + str(website) + "\");"

		# run the insert statement on the database
		self.cursor.execute(insert_statement)
		self.conn.commit()

	def insert_stadiums(self, stadium_dict):
		stadium_name = stadium_dict['stadium name']
		try:
			capacity = stadium_dict['Capacity']
		except KeyError:
			# West Brom's stadium has 'The Hawthorns capacity' as its capacity
			capacity = stadium_dict['The Hawthorns capacity']

		capacity = capacity.replace(',', '')
		try:
			record_pl_attendance = stadium_dict['Record PL attendance']
		except KeyError as kerr:
			record_pl_attendance = 'Null'

		address = stadium_dict['Stadium address']
		pitch_size = stadium_dict['Pitch size']
		built = stadium_dict['Built']
		try:
			phone = stadium_dict['Phone']
		except KeyError:
			try:
				phone = stadium_dict['Phone - International']
			except KeyError:
				phone = stadium_dict['International Phone']

		insert_statement = "INSERT INTO stadium (stadium_name, capacity, record_pl_attendance, address, pitch_size, built, phone) "
		insert_statement += "VALUES(\"" + str(stadium_name) + "\", "
		insert_statement += "" + str(capacity) + ", "
		insert_statement += "\"" + str(record_pl_attendance) + "\", "
		insert_statement +=	"\"" + str(address) + "\", "
		insert_statement += "\"" + str(pitch_size) + "\", "
		insert_statement += "" + str(built) + ", "
		insert_statement += "\"" + str(phone) + "\");"

		self.cursor.execute(insert_statement)
		self.conn.commit()

	def insert_match_basic_info(self, match_basic_info_dict, date_dict):
		match_id = match_basic_info_dict['match id']
		home_team_name = match_basic_info_dict['home']
		away_team_name = match_basic_info_dict['away']

		# get the home and away team ids
		home_club_id_query = "SELECT club_id FROM club "
		home_club_id_query += "WHERE club_name=" + home_team_name + ";"
		
		# execute the query to get the id of the home club
		self.cursor.execute(home_club_id_query)
		tuple_list = self.cursor.fetchall()
		home_team_id = tuple_list[0][0]

		away_club_id_query = "SELECT club_id FROM club "
		away_club_id_query += "WHERE club_name=" + away_club_name + ";"

		# execute the query to get the id of the away club
		self.cursor.execute(away_club_id_query)
		tuple_list = self.cursor.fetchall()
		away_club_id = tuple_list[0][0]

		home_goals = match_basic_info_dict['home goals']
		away_goals = match_basic_info_dict['away goals']
		stadium_name = match_basic_info_dict['stadium name']
		city = match_basic_info_dict['city']

	# this function helps us clear all the rows of a table in case the 
	#	after we do test insert statements
	def delete_all_rows(self, table_name):
		delete_statement = "DELETE FROM " + table_name

		self.cursor.execute(delete_statement)
		self.conn.commit()

	# club name->Aston Villa
	# stadium name->Villa Park
	# website->www.avfc.co.uk
	# Capacity->42,682
	# Built->1897
	# Pitch size->105m x 68m
	# Stadium address->Villa Park, Trinity Road, Birmingham, B6 6HE
	# Phone - UK->0333 323 1874
	# Phone - International->+44 (0)121 327 5353




# Have functions that do the queries to obtain the following player/club stats:
# calculate the following:
# points (league standings)
# goals_scored
# own goals conceded
# goals conceded
# clean sheats 
# wins
# losses
# draws
# passes
# shots
# shooting accuracy 
# shots on target
# penalties scored, 
# offsides
# yellow cards
# red cards
# fouls