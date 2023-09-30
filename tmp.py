from database_helper import *
import sqlite3
conn = sqlite3.connect("invalidAddress.db")
cursor = conn.cursor()
cursor.execute(f"SELECT history FROM invalidAddress")
results = cursor.fetchall()