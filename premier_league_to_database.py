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

	def insert_managers(self, managers_list_of_dict):
		insert_statement = "INSERT INTO managers()"
		for manager in managers_list_of_dict:
			print(manager['manager name'])
			print(manager['Country of Birth'])

	def insert_players(self, players_list_of_dict):
		insert_statement = "INSERT INTO players"

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