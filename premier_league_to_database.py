import mysql.connector as connector
from mysql.connector import Error
from mysql.connector import IntegrityError
from connect_to_database import *


# handles all the database related work.
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

	# @parameters:
	#		managers_dict = contains the manaeger-specific data, such as name, country, dob, etc
	#		season = used for inserting the manager into the manager_club table. Tells us the
	#			season in which the manager has been in the club
	def insert_managers(self, managers_dict):
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
			joined_club_month = self.convert_month_to_number(joined_club_month)

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

		# use the get_id function to see if the manager already is in the database
		manager_id = self.get_id(manager_name, 'manager')

		# if no manager with that name was found (id = 'Null'), insert the manager
		if manager_id == 'Null':
			insert_statement = "INSERT INTO manager(manager_name, country, active, joined_club, date_of_birth, epl_seasons, epl_debut_match) "
			insert_statement += "VALUES(\"" + str(manager_name) + "\", "
			insert_statement += "\"" + str(country) + "\", "
			insert_statement += str(active) + ", "
			insert_statement += "\"" + joined_club_date + "\", "
			insert_statement += "\"" + dob_date + "\", "
			insert_statement += "\"" + epl_seasons + "\", "
			insert_statement += "\"" + epl_debut_match + "\");"

			self.cursor.execute(insert_statement)
			self.conn.commit()

		else:
			print(manager_name + ' already in manager table.')

	
	def insert_manager_club(self, manager_name, club_name, season):
		# get the id of the manager that just got inserted into the table
		manager_id = self.get_id(manager_name, 'manager')

		if club_name == "Bournemouth":
			club_name = "AFC Bournemouth"

		# get the id of the club
		club_id = self.get_id(club_name, 'club')
		
		# update the manager_club table
		try:
			insert_statement = "INSERT INTO manager_club(manager_id, club_id, season) "
			insert_statement += "VALUES(" + str(manager_id) + ", "
			insert_statement += str(club_id) + ", "
			insert_statement += "\"" + season + "\");"

			self.cursor.execute(insert_statement)
			self.conn.commit()

		except IntegrityError:
			print(manager_name + ' ' + str(club_id) + ' ' + season + ' already in manager_club.')


	def insert_players(self, player_dict):
		player_name = player_dict['player name']
		position = player_dict['position']
		country = player_dict['country']
		season = player_dict['season']

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
		
		# Some players have label.substitute as the position. In that case,
		#		insert 'Null' for the position.
		if len(position) > 12:
			position = 'Null'

		player_id = self.get_id(player_name, 'player')

		# if the player name is not in the database (player_id='Null'), then insert
		#		the player
		if player_id == 'Null':
			insert_statement = "INSERT INTO player(player_name, player_number, position, country, date_of_birth, height) "
			insert_statement += "VALUES(\"" + player_name + "\", "
			insert_statement += str(shirt_number) + ", "
			insert_statement += "\"" + position + "\", "
			insert_statement += "\"" + country + "\", "
			insert_statement += "\"" + dob_date + "\", "
			insert_statement += str(height) + ");"

			self.cursor.execute(insert_statement)
			self.conn.commit()

			player_id = self.get_id(player_name, 'player')
		else:
			print(player_name + ' already in player table.')

		# player_dict['clubs'] is a dictionary
		club_names = player_dict['clubs']



		for season, club_name_list in club_names.items():
			for club_name in club_name_list:
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

				# get the club id of the player
				club_id = self.get_id(club_name, 'club')

				try:
					insert_statement = "INSERT INTO player_club(player_id, club_id, season) "
					insert_statement += "VALUES(" + str(player_id) + ", "
					insert_statement += str(club_id) + ", "
					insert_statement += "\"" + season + "\");"

					self.cursor.execute(insert_statement)
					self.conn.commit()

				except IntegrityError:
					print(player_name + ' ' + str(club_name) + ' ' + season + ' already in player_club.')
		
		# see if the career table is ever empty. Remove later.
		if len(club_names) == 0:
			print(player_name + ' has no clubs in the career table.')
	# get the stadium_name to obtain stadium_id from the stadium table
	def insert_clubs(self, club_dict):
		club_name = club_dict['club name']
		website = club_dict['website']

		# get the stadium id from the stadium table using get_id function
		stadium_name = club_dict['stadium name']
		stadium_id = self.get_id(stadium_name, 'stadium')
		
		insert_statement = "INSERT INTO club (stadium_id, club_name, website) "
		insert_statement += "VALUES(" + str(stadium_id) + ", "
		insert_statement += "\"" + str(club_name) + "\", "
		insert_statement += "\"" + str(website) + "\");"

		# run the insert statement on the database
		self.cursor.execute(insert_statement)
		self.conn.commit()

	def insert_stadiums(self, stadium_dict):
		stadium_name = stadium_dict['stadium name']
		
		stadium_id = self.get_id(stadium_name, 'stadium')

		# if the stadium is not in the database
		if stadium_id == 'Null':

			capacity_keys = [key for key, val in stadium_dict.items() if 'capacity' in key or 'Capacity' in key]
			print(capacity_keys)
			capacity = stadium_dict[capacity_keys[0]]

			if 'Capacity' in stadium_dict.keys():
				capacity = stadium_dict['Capacity']
			# West Brom's stadium has 'The Hawthorns capacity' as its capacity
			elif 'The Hawthorns capacity' in stadium_dict.keys():
				capacity = stadium_dict['The Hawthorns capacity']
			# AFC Bournemouth's stadium has the capacity key below
			elif 'Viality Stadium capacity 2018/19' in stadium_dict.keys():
				capacity = stadium_dict['Viality Stadium capacity 2018/19']

			capacity = capacity.replace(',', '')
			
			try:
				record_pl_attendance = stadium_dict['Record PL attendance']
			except KeyError as kerr:
				record_pl_attendance = 'Null'

			address = stadium_dict['Stadium address']
			pitch_size = stadium_dict['Pitch size']
			built = stadium_dict['Built']
			
			if 'Phone' in stadium_dict.keys():
				phone = stadium_dict['Phone']
			elif 'Phone - International' in stadium_dict.keys():
				phone = stadium_dict['Phone - International']
			elif 'International Phone' in stadium_dict.keys():
				phone = stadium_dict['International Phone']
			elif 'Phone - UK' in stadium_dict.keys():
				phone = stadium_dict['Phone - UK']

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
		else:
			print('Stadium ' + stadium_name + ' already in the database.')

	# takes in the match information and date of the match (including
	#	the referee's name), and inserts the information into the match_
	#	table
	def insert_match_basic_info(self, match_basic_info_dict, date_dict):
		match_id = match_basic_info_dict['match id']
		home_club_name = match_basic_info_dict['home']
		away_club_name = match_basic_info_dict['away']
		season = match_basic_info_dict['season']

		# get the home and away team ids
		home_club_id = self.get_id(home_club_name, 'club')
		away_club_id = self.get_id(away_club_name, 'club')

		home_goals = match_basic_info_dict['home goals']
		away_goals = match_basic_info_dict['away goals']
		stadium_name = match_basic_info_dict['stadium name']

		# get the stadium_id from stadium_name using get_id() function
		stadium_id = self.get_id(stadium_name, 'stadium')

		city = match_basic_info_dict['city']

		month_name = date_dict['month']
		month = self.convert_month_to_number(month_name)
		day = date_dict['day']
		year = date_dict['year']

		match_date = year + '-' + month + '-' + day

		referee_name = date_dict['referee']

		matchweek = date_dict['matchweek']

		insert_statement_match_ = "INSERT INTO match_(match_id, home_team_id, away_team_id, home_team_goals, away_team_goals, match_date, matchweek, referee, stadium_id, season) "
		insert_statement_match_ += "VALUES("
		insert_statement_match_ += str(match_id) + ", "
		insert_statement_match_ += str(home_club_id) + ", "
		insert_statement_match_ += str(away_club_id) + ", "
		insert_statement_match_ += str(home_goals) + ", "
		insert_statement_match_ += str(away_goals) + ", "
		insert_statement_match_ += "\"" + str(match_date) + "\", "
		insert_statement_match_ += str(matchweek) + ", "
		insert_statement_match_ += "\"" + str(referee_name) + "\", "
		insert_statement_match_ += str(stadium_id) + ", "
		insert_statement_match_ += "\"" + str(season) + "\");"

		try:
			print(insert_statement_match_)
			self.cursor.execute(insert_statement_match_)
			self.conn.commit()

		except IntegrityError:
			print('Duplicate entry exception')
			raise

	# receives the stats of both teams, the match id, and the id of both
	#	clubs match_id_and_club_names[0] = match_id 
	#		  match_id_and_club_names[1] = home club_id
	#		  match_id_and_club_names[2] = away club_id
	def insert_club_stats(self, club_stats_dict, match_id_and_club_names):
		match_id = match_id_and_club_names[0]
		club_home_name = match_id_and_club_names[1]
		club_away_name = match_id_and_club_names[2]
		season = match_id_and_club_names[3]

		club_home_id = self.get_id(club_home_name, 'club')
		club_away_id = self.get_id(club_away_name, 'club')

		# use the helper function to get the match stats
		possession_home, possession_away = self.insert_club_stats_helper(club_stats_dict, 'Possession', season)
		shots_on_target_home, shots_on_target_away = self.insert_club_stats_helper(club_stats_dict, 'Shots on target', season)
		shots_home, shots_away = self.insert_club_stats_helper(club_stats_dict, 'Shots', season)
		touches_home, touches_away = self.insert_club_stats_helper(club_stats_dict, 'Touches', season)
		passes_home, passes_away = self.insert_club_stats_helper(club_stats_dict, 'Passes', season)
		tackles_home, tackles_away = self.insert_club_stats_helper(club_stats_dict, 'Tackles', season)
		clearances_home, clearances_away = self.insert_club_stats_helper(club_stats_dict, 'Clearances', season)
		corners_home, corners_away = self.insert_club_stats_helper(club_stats_dict, 'Corners', season)
		offsides_home, offsides_away = self.insert_club_stats_helper(club_stats_dict, 'Offsides', season)
		fouls_conceded_home, fouls_conceded_away = self.insert_club_stats_helper(club_stats_dict, 'Fouls conceded', season)
		yellow_cards_home, yellow_cards_away = self.insert_club_stats_helper(club_stats_dict, 'Fouls conceded', season)
		red_cards_home, red_cards_away = self.insert_club_stats_helper(club_stats_dict, 'Red cards', season)

		# insert statement for the home side
		insert_statement = "INSERT INTO club_stats(match_id, club_id, possession, shots, shots_on_target, touches, passes, tackles, clearances, corners, offsides, fouls_conceded, yellow_cards, red_cards) "
		insert_statement += "VALUES(" + str(match_id) + ", "
		insert_statement += str(club_home_id) + ", "
		insert_statement += str(possession_home) + ", "
		insert_statement += str(shots_home) + ", "
		insert_statement += str(shots_on_target_home) + ", "
		insert_statement += str(touches_home) + ", "
		insert_statement += str(passes_home) + ", "
		insert_statement += str(tackles_home) + ", "
		insert_statement += str(clearances_home) + ", "
		insert_statement += str(corners_home) + ", "
		insert_statement += str(offsides_home) + ", "
		insert_statement += str(fouls_conceded_home) + ", "
		insert_statement += str(yellow_cards_home) + ", "
		insert_statement += str(red_cards_home) + ");"

		self.cursor.execute(insert_statement)
		self.conn.commit()

		# insert statement for the away side
		insert_statement = "INSERT INTO club_stats(match_id, club_id, possession, shots, shots_on_target, touches, passes, tackles, clearances, corners, offsides, fouls_conceded, yellow_cards, red_cards) "
		insert_statement += "VALUES(" + str(match_id) + ", "
		insert_statement += str(club_away_id) + ", "
		insert_statement += str(possession_away) + ", "
		insert_statement += str(shots_away) + ", "
		insert_statement += str(shots_on_target_away) + ", "
		insert_statement += str(touches_away) + ", "
		insert_statement += str(passes_away) + ", "
		insert_statement += str(tackles_away) + ", "
		insert_statement += str(clearances_away) + ", "
		insert_statement += str(corners_away) + ", "
		insert_statement += str(offsides_away) + ", "
		insert_statement += str(fouls_conceded_away) + ", "
		insert_statement += str(yellow_cards_away) + ", "
		insert_statement += str(red_cards_away) + ");"


		self.cursor.execute(insert_statement)
		self.conn.commit()

	# @arguments:
	#	a dictionary with player name as the key, and the performance
	#		of the minute as an array value
	def insert_player_performance(self, player_performance_dict, match_id):

		# iterate through the player performances
		for player_name, performance_array_of_arrays in player_performance_dict.items():
			print(player_name)
			player_id = self.get_id(player_name, 'player')
			# some players have not appeared in the player's page, and thus have
			#	no player_id

			if player_id == 'Null':
				print(player_name + ' has no player_id')

				# insert the player
				insert_player_statement = "INSERT INTO player(player_name) "
				insert_player_statement += "VALUES(\"" + player_name + "\");"

				self.cursor.execute(insert_statement)
				self.conn.commit()

			# goal (goal) = 1
			# goal penalty = 2
			# assist (assist) = 3
			# own goal = 4
			# red card = 5
			# Second Yellow Card (Red Card) = 6
			for performance_array in performance_array_of_arrays:
				print(performance_array)
				if performance_array[1] == 'goal':
					type_of_stat = 1
				elif performance_array[1] == 'goal penalty':
					type_of_stat = 2
				elif performance_array[1] == 'assist':
					type_of_stat = 3
				elif performance_array[1] == 'own goal':
					type_of_stat = 4
				elif performance_array[1] == 'red card':
					type_of_stat = 5
				elif performance_array[1] == 'Second Yellow Card (Red Card)':
					type_of_stat = 6

				minutes = []
				for i in range(2, len(performance_array)):
					minutes.append(performance_array[i])

				for minute in minutes:
					insert_statement = "INSERT INTO player_performance(player_id, match_id, type_of_stat, minute) "
					insert_statement += "VALUES(" + str(player_id) + ", "
					insert_statement += str(match_id) + ", "
					insert_statement += str(type_of_stat) + ", "
					insert_statement += "\"" + minute + "\");"

					self.cursor.execute(insert_statement)
					self.conn.commit()


	# @arguments:
	#	dictionary of dictionaries for player stats, with the key of the 
	#	outer dictionary being the name of the player
	def insert_player_stats(self, player_stats_dict_of_dicts, match_id):
		for key_player_name, player_stats_dict in player_stats_dict_of_dicts.items():
			player_name = key_player_name
			player_id = self.get_id(player_name, 'player')
			
			is_in_starting_11 = player_stats_dict['Starting 11']
			substitution_on = player_stats_dict['Substitution On']
			substitution_off = player_stats_dict['Substitution Off']
			yellow_card = player_stats_dict['Yellow Card']
			red_card = player_stats_dict['Red Card']

			insert_statement = "INSERT INTO player_stats(player_id, match_id, is_in_starting_11, substitution_on, substitution_off, yellow_card, red_card) "
			insert_statement += "VALUES(" + str(player_id) + ", "
			insert_statement += str(match_id) + ", "
			insert_statement += str(is_in_starting_11) + ", "
			insert_statement += "\"" + str(substitution_on) + "\", "
			insert_statement += "\"" + str(substitution_off) + "\", "
			insert_statement += "\"" + str(yellow_card) + "\", "
			insert_statement += "\"" + str(red_card) + "\");"

			if player_id != 'Null':				
				self.cursor.execute(insert_statement)
				self.conn.commit()
			else:
				print('************************Null player_id')
				print('inserting ' + player_name + ' into db.')
				
				print(player_name)

	def update_stadium_city(self, stadium_city_dict):
		key_list = list(stadium_city_dict.keys())
		value_list = list(stadium_city_dict.values())

		stadium_name = key_list[0]
		city = value_list[0]

		# get the stadium_id from stadium_name using get_id() function
		stadium_id = self.get_id(stadium_name, 'stadium')

		update_city_of_stadium = "UPDATE stadium "
		update_city_of_stadium += "SET city=\"" + city + "\" "
		update_city_of_stadium += "WHERE stadium_id=" + str(stadium_id) + ";"

		self.cursor.execute(update_city_of_stadium)
		self.conn.commit()


	# convert the month name into number from 01 to 12
	def convert_month_to_number(self, month):
		if month == "January" or month == "Jan":
			month = '01'
		elif month == "February" or month == "Feb":
			month = '02'
		elif month == 'March' or month == "Mar":
			month = '03'
		elif month == 'April' or month == "Apr":
			month = '04'
		elif month == 'May' or month == "May":
			month = '05'
		elif month == 'June' or month == "Jun":
			month = '06'
		elif month == 'July' or month == "Jul":
			month = '07'
		elif month == 'August' or month == "Aug":
			month = '08'
		elif month == 'September' or month == "Sep":
			month = '09'
		elif month == 'October' or month == "Oct":
			month = '10'
		elif month == 'November' or month == "Nov":
			month = '11'
		elif month == 'December' or month == "Dec":
			month = '12'
		
		return month

	# @arguments:
	#	the name of the entity, such as club_name, player_name, stadium_name
	#	the name of the table
	# @returns:
	#	depending on the table name:
	#	if table_name == player: return player_id
	#	if table_name == club: return club_id
	#	if table_name == stadium: return stadium_id
	def get_id(self, name, table_name):
		# id_string = player_id/club_id/stadium_id
		id_str = table_name + '_id'
		# name_str = player_name/club_name/stadium_name
		name_str = table_name + '_name'

		club_id_query = "SELECT " + id_str + " FROM " + table_name + " "
		club_id_query += "WHERE " + name_str + "=\"" + name + "\";"

		self.cursor.execute(club_id_query)
		tuple_list = self.cursor.fetchall()
		
		try:
			club_id = tuple_list[0][0]
		except IndexError:
			club_id = 'Null'

		return club_id

	# this function helps us clear all the rows of a table in case the 
	#	after we do test insert statements
	def delete_all_rows(self, table_name):
		delete_statement = "DELETE FROM " + table_name

		self.cursor.execute(delete_statement)
		self.conn.commit()

	# get all the match_ids already inserted to make the results_scraper faster
	# 	returns match_ids as a list
	def get_all_match_ids_inserted(self):
		query = "SELECT match_id FROM match_"

		self.cursor.execute(query)
		match_ids = self.cursor.fetchall()

		list_of_match_ids = []

		for match_id_tuple in match_ids:
			match_id = match_id_tuple[0]
			list_of_match_ids.append(match_id)

		return list_of_match_ids

	# get all the player names already inserted
	def get_all_players_inserted(self):
		query = "SELECT player_name FROM player;"

		self.cursor.execute(query)
		player_names = self.cursor.fetchall()

		list_of_player_names = []

		for player_name_tuple in player_names:
			player_name = player_name_tuple[0]
			list_of_player_names.append(player_name)

		return list_of_player_names
	
	# @parameters
	#		accepts the dictionary for the match stats and the key to look for.
	# @returns the values found corresponding to the keys
	# 		if the results are not found, returns 0's
	# 		if there are no such stats (such as when the season is older than
	#			the 2006/07 season), then return Null's
	def insert_club_stats_helper(self, club_stats_dict, key, season):
		# if the result is from the season prior to 1995/96, then there are no 
		#		stats provided
		if season < '2006/07':
			return 'Null', 'Null'
		else:
			try:
				value_home = club_stats_dict[key + ' home']
				value_away = club_stats_dict[key + ' away']
				return value_home, value_away
			except KeyError:
				return 0, 0

	def get_player_clubs(self, season):
		query = "SELECT p.player_name, p_c.season "
		query += "FROM player_club AS p_c INNER JOIN player as p ON p_c.player_id=p.player_id WHERE p_c.season=\"" + str(season) + "\";"

		self.cursor.execute(query)
		tuple_list = self.cursor.fetchall()
		player_club_list_of_dicts = self.convert_from_tuple_list_to_dict(tuple_list)

		return player_club_list_of_dicts


	def get_top_players(self, number_of_rows, type_of_stat):
		query = "SELECT p.player_name, count(p_p.player_id) as number_of_goals FROM player as p, player_performance as p_p "
		query += "WHERE p.player_id=p_p.player_id and p_p.type_of_stat=1"
		# goal (goal) = 1
		# goal penalty = 2
		# assist (assist) = 3
		# own goal = 4
		# red card = 5
		# Second Yellow Card (Red Card) = 6
		if type_of_stat == 'all goals':
			type_of_stat = "1 or type_of_stat=2"
			order_by = 'All_Goals'
		elif type_of_stat == 'goals':
			type_of_stat = 1
			order_by = 'Goals'
		elif type_of_stat == 'penalty goals':
			type_of_stat = 2
		elif type_of_stat == 'assists':
			type_of_stat = 3
			order_by = 'Assists'
		elif type_of_stat == 'own goals':
			type_of_stat = 4
			order_by = 'Own_Goals'
		elif type_of_stat == 'red cards':
			type_of_stat = 5
			order_by = 'Red_Cards'
		elif type_of_stat == 'second yellow card':
			type_of_stat = 6
			order_by = 'Second_Yellow_Cards'


		query = "SELECT player_name as \"Player Name\", c.club_name as Club, count(*) as " + order_by + " "
		query += "FROM player_performance as pp " 
		query += "INNER JOIN player as p ON pp.player_id=p.player_id "
		query += "INNER JOIN club as c on p.club_id=c.club_id "
		query += "WHERE (type_of_stat=" + str(type_of_stat) + ") "
		query += "GROUP BY p.player_id "
		query += "ORDER BY " + order_by + " desc "
		query += "limit " + str(number_of_rows);



		self.cursor.execute(query)
		tuple_list = self.cursor.fetchall()

		list_of_dicts = self.convert_from_tuple_list_to_dict(tuple_list)
		
		for dict_ in list_of_dicts:
			print(dict_)

	def get_appearances(self, number_of_rows):
		# get the player's club
		#	 select p.player_name as Player, c.club_name as Club, count(p.player_name) as Appearances from player_stats as p_s INNER JOIN player as p on p.player_id=p_s.player_id INNER JOIN club as c on p.club_id=c.club_id where p_s.is_in_starting_11=1 or p_s.substitution_on!=Null group by p.player_id order by Appearances desc limit 10;
		query = "SELECT p.player_name as Player, c.club_name as Club, count(p.player_name) as Appearances "
		query += "FROM player_stats as p_s "
		query += "INNER JOIN player as p on p.player_id=p_s.player_id "
		query += "INNER JOIN club as c on p.club_id=c.club_id "
		query += "WHERE p_s.is_in_starting_11=1 or p_s.substitution_on!=Null "
		query += "GROUP BY p.player_id "
		query += "ORDER BY Appearances DESC "
		query += "limit " + str(number_of_rows) + ";"

		self.cursor.execute(query)
		tuple_list = self.cursor.fetchall()

		tuple_list = convert_from_tuple_list_to_dict(tuple_list)
		print(tuple_list)
		
		list_of_dicts = self.convert_from_tuple_list_to_dict(tuple_list)
		
		for dict_ in list_of_dicts:
			print(dict_)


	def convert_from_tuple_list_to_dict(self, tuple_list):
		if len(tuple_list) > 0:
			list_of_dicts = []

			# get the column names of the returned query
			columns = [column[0] for column in self.cursor.description]

			for row in tuple_list:
				list_of_dicts.append(dict(zip(columns, row)))

				# list_of_dict.append(dict(zip(columns, row)))

			return list_of_dicts

		else:
			print('Empty set returned.')
			return []

	def generate_standings(self):
		# position, club, played, won, drawn, lost, gf, ga, gd, points, form (earliest-.-.-.-newest)
		query_won = "SELECT c.club_name, count(*) as wins "
		query_won += "FROM match_ as m "
		query_won += "INNER JOIN club as c "
		query_won += "on (m.home_team_id=c.club_id and m.home_team_goals>m.away_team_goals) "
		query_won += "or (m.away_team_id=c.club_id and m.away_team_goals>m.home_team_goals) "
		query_won += "GROUP BY c.club_name " 
		query_won += "ORDER BY wins DESC;"
		
		self.cursor.execute(query_won)
		tuple_list = self.cursor.fetchall()

		list_of_dicts = self.convert_from_tuple_list_to_dict(tuple_list)

		wins_dict = {}

		for dict_ in list_of_dicts:
			wins_dict[dict_['club_name']] = dict_['wins']
			
		# Now get the information about draws. Just replace the > sign with =
		#		to compare the number of goals scored in the match.
		query_drawn = query_won.replace('>', '=')
		query_drawn = query_drawn.replace('wins', 'draws')

		self.cursor.execute(query_drawn)
		tuple_list = self.cursor.fetchall()

		list_of_dicts = self.convert_from_tuple_list_to_dict(tuple_list)

		draws_dict = {}

		for dict_ in list_of_dicts:
			draws_dict[dict_['club_name']] = dict_['draws']

		# Get the losses of each team. reuse the query_won
		query_lost = query_won.replace('wins', 'lost')
		query_lost = query_lost.replace('>', '<')

		self.cursor.execute(query_lost)
		tuple_list = self.cursor.fetchall()

		list_of_dicts = self.convert_from_tuple_list_to_dict(tuple_list)

		lost_dict = {}

		for dict_ in list_of_dicts:
			lost_dict[dict_['club_name']] = dict_['lost']

		# Get the goals scored
		# Count either the home_team_goals or the away_team_goals, based on
		#		whether the current team is the host or the guest. 
		query_goals_for = "SELECT c.club_name, "
		query_goals_for += "sum(case when m.home_team_id=c.club_id then m.home_team_goals "
		query_goals_for += "else m.away_team_goals end) as goals_for "
		query_goals_for += "FROM match_ as m INNER JOIN club as c "
		query_goals_for += "on (m.home_team_id=c.club_id) or (m.away_team_id=c.club_id) "
		query_goals_for += "GROUP BY c.club_name ORDER BY goals_for desc;"
		
		self.cursor.execute(query_goals_for)
		tuple_list = self.cursor.fetchall()

		list_of_dicts = self.convert_from_tuple_list_to_dict(tuple_list)

		goals_for_dict = {}

		for dict_ in list_of_dicts:
			goals_for_dict[dict_['club_name']] = int(dict_['goals_for'])


		# get the goals conceded
		query_goals_against = query_goals_for.replace('then m.home_team_goals', 'then m.away_team_goals')
		query_goals_against = query_goals_against.replace('else m.away_team_goals', 'else m.home_team_goals')
		query_goals_against = query_goals_against.replace('goals_for', 'goals_against')

		self.cursor.execute(query_goals_against)
		tuple_list = self.cursor.fetchall()

		list_of_dicts = self.convert_from_tuple_list_to_dict(tuple_list)

		goals_against_dict = {}

		for dict_ in list_of_dicts:
			goals_against_dict[dict_['club_name']] = int(dict_['goals_against'])

		goal_difference_dict = {}
		
		for key_team_name, value_goals_scored in goals_for_dict.items():
			# calculate the goal difference of the team and store it into the
			#		goal_difference_dict
			goal_difference_dict[key_team_name] = value_goals_scored - goals_against_dict[key_team_name]

		team_points = {}
		for key_team_name, value_number_of_wins in wins_dict.items():
			team_points[key_team_name] = 3*value_number_of_wins + draws_dict[key_team_name]

		# sort the dictionary by points
		team_points = dict(sorted(team_points.items(), key=lambda item: item[1], reverse=True))

		

		# # get the matchweek (last 5), home and away teams, and the winner
		# #	team name (value=draw if no winner)
		# # using only the matchweek>33 does not work because the matchweek numbers
		# #	are not consistent.
		# # get the last 5 match results of each team programatically
		# query_form_last_5 = "SELECT matchweek, club_home.club_name AS Home, "
		# query_form_last_5 += "club_away.club_name AS Away, "
		# query_form_last_5 += "(CASE WHEN home_team_goals>away_team_goals then club_home.club_name "
		# query_form_last_5 += "WHEN home_team_goals=away_team_goals then \"draw\" "
		# query_form_last_5 += "ELSE club_away.club_name end) AS winner "
		# query_form_last_5 += "FROM match_ INNER JOIN club AS club_home ON club_home.club_id=home_team_id "
		# query_form_last_5 += "INNER JOIN club AS club_away ON club_away.club_id=away_team_id "
		# query_form_last_5 += "WHERE matchweek>33 "
		# query_form_last_5 += "ORDER BY matchweek asc;"

		# Get the id of each team
		query_club_ids = "SELECT club_id, club_name from club;"
		self.cursor.execute(query_club_ids)
		tuple_list = self.cursor.fetchall()
		list_of_dicts_clubs = self.convert_from_tuple_list_to_dict(tuple_list)
		
		form_last_5_dict = {}

		# set up the form dictionary to fill in later
		# the dictionary key numbers 34 through 38 represent the matchweek.
		#		their values will either be W, D, or L, for Win, Draw, or Loss,
		#		respectively.
		for team in team_points.keys():
			form_last_5_dict[team] = {} 		

		for id_dict in list_of_dicts_clubs:
			club_id = id_dict.get('club_id')
			club_name = id_dict.get('club_name')
			# Get the last 5 matches of each team
			query_form_last_5 = "SELECT m.matchweek, c_h.club_name AS Home, m.home_team_goals, "
			query_form_last_5 += "m.away_team_goals, c_a.club_name AS Away, "
			query_form_last_5 += "(CASE WHEN m.home_team_goals>m.away_team_goals then c_h.club_name "
			query_form_last_5 += "WHEN m.home_team_goals=m.away_team_goals then \"draw\" "
			query_form_last_5 += "ELSE c_a.club_name END) AS winner "
			query_form_last_5 += "FROM match_ AS m "
			query_form_last_5 += "INNER JOIN club AS c_h ON c_h.club_id=m.home_team_id "
			query_form_last_5 += "INNER JOIN club AS c_a on c_a.club_id=m.away_team_id "
			query_form_last_5 += "WHERE home_team_id=" + str(club_id) + " or away_team_id=" + str(club_id) + " "
			query_form_last_5 += "ORDER BY match_date desc "
			query_form_last_5 += "LIMIT 5;"


			self.cursor.execute(query_form_last_5)
			tuple_list = self.cursor.fetchall()
			list_of_dicts_last_5 = self.convert_from_tuple_list_to_dict(tuple_list)
			
			# print(list_of_dicts_last_5)

			# extract the last 5 match results
			matchweek = 38
			for result in list_of_dicts_last_5:
				if result['winner'] == club_name:
					form_last_5_dict[club_name][matchweek] = 'W'
				elif result['winner'] != 'draw':
					form_last_5_dict[club_name][matchweek] = 'L'
				else:
					form_last_5_dict[club_name][matchweek] = 'D'
				matchweek -= 1

		table_list_of_dicts = []

		table_position = 0
		# combine all the table information together into table_list_of_dicts
		for key_club_name, value in form_last_5_dict.items():
			# print(key_club_name, end="  ")
			
			table_list_of_dicts.append({})
			# add the team information to the table
			table_list_of_dicts[table_position]['team_name'] = key_club_name
			table_list_of_dicts[table_position]['num_of_wins'] = wins_dict[key_club_name]
			table_list_of_dicts[table_position]['num_of_draws'] = draws_dict[key_club_name]
			table_list_of_dicts[table_position]['num_of_losses'] = lost_dict[key_club_name]
			table_list_of_dicts[table_position]['goals_for'] = goals_for_dict[key_club_name]
			table_list_of_dicts[table_position]['goals_against'] = goals_against_dict[key_club_name]
			table_list_of_dicts[table_position]['goal_difference'] = goal_difference_dict[key_club_name]
			table_list_of_dicts[table_position]['team_points'] = team_points[key_club_name]
			table_list_of_dicts[table_position]['form'] = ''

			# for key_last_5 in sorted(value):
			for matchweek, w_d_l in value.items():
				# append to the result from the left
				table_list_of_dicts[table_position]['form'] = w_d_l + table_list_of_dicts[table_position]['form']
			
			

			table_position += 1

		self.print_table(table_list_of_dicts)

	def print_table(self, table_list_of_dicts):
		for row_dict in table_list_of_dicts:
			print(row_dict['team_name'], end="  ")
			print(row_dict['num_of_wins'], end="  ")
			print(row_dict['num_of_draws'], end="  ")
			print(row_dict['num_of_losses'], end="  ")
			print(row_dict['goals_for'], end="  ")
			print(row_dict['goals_against'], end="  ")
			print(row_dict['goal_difference'], end="  ")
			print(row_dict['team_points'], end="  ")
			print(row_dict['form'], end="  ")
			print()

# !!! get the missing players from from the player_stats and insert them into the
#		players table

# Have functions that do the queries to obtain the following player/club stats:
# calculate the following:
# points (league standings)
# own goals conceded
# average of those:
	# goals conceded
	# clean sheats 
	# passes
	# shots
	# shooting accuracy 
	# shots on target
	# penalties scored, 
	# offsides
	# yellow cards
	# red cards
	# fouls