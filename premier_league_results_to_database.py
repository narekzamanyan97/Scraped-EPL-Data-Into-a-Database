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
		insert_query_str = "INSERT INTO managers()"
		for manager in managers_list_of_dict:
			print(manager['manager name'])
			print(manager['Country of Birth'])

	def insert_players(self, players_list_of_dict):
		




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