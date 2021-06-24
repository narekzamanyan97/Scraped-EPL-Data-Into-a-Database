import mysql.connector as connector
from mysql.connector import Error

def connect_to_database():
	try:
		connection = connector.connect(host='localhost',
									database='premier_league',
									user='root',
									password='',
									auth_plugin='mysql_native_password')

	