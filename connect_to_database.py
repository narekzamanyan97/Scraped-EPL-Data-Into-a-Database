import mysql.connector as connector
from mysql.connector import Error

def connect_to_database():
	try:
		connection = connector.connect(host='localhost',
									database='premier_league',
									user='root',
									password='narekpassword',
									auth_plugin='mysql_native_password')
		
	except Error as e:
		print("An error has occured. Message: " + str(e))
	else:
		print("Connection successful.")
		return connection
