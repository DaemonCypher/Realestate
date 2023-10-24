import sqlite3
import json 

def fetch_specific_from_db(conn,table_name,column):
    """ 
    Fetch all values from a specific column in a given database table.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite3 database.
        table_name (str): Name of the database table to fetch data from.
        column (str): Name of the column to fetch values from.

    Returns:
        list[tuple]: A list containing tuples, where each tuple has a value from the specified column.
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT {column} FROM {table_name}")
    results = cursor.fetchall()
    return results

def fetch_from_db(conn, table_name):
    """
    Retrieve all values from a specified database table.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite3 database.
        table_name (str): Name of the database table to fetch data from.

    Returns:
        list[tuple]: List of tuples with data from the specified table. Each tuple contains:
            - id (int): Unique identifier for the record.
            - address (str): Property address.
            - city (str): City where the property is located.
            - history (list): List of property history data.
            - status (str): Current property status.
            - status_date (str): Date of the last status update.
            - data_date (str): Date of the last data fetch/update.
            - beds (int): Number of bedrooms in the property.
            - baths (int): Number of bathrooms in the property.
            - yearBuilt (int): Year when the property was constructed.
            - sqft (int): Property's square footage.
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, address, city, history, status, statusDate, dataDate, beds, baths, yearBuilt, sqft FROM {table_name}")
    results = cursor.fetchall()

    deserialized_results = []
    for row in results:
        id, address, city, history_str, status, status_date, data_date, beds, baths, year_built, sqft = row
        # Deserialize the history field
        history = json.loads(history_str)
        deserialized_results.append((id, address, city, history, status, status_date, data_date, beds, baths, year_built, sqft))
    return deserialized_results

def add_column_to_table(conn, table_name, column_name, column_type):
    """
    Add a new column to an existing table in the database.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite3 database.
        table_name (str): Name of the table to add the column to.
        column_name (str): Name of the new column to be added.
        column_type (str): Data type of the new column (e.g., 'TEXT', 'INTEGER', 'REAL').

    Raises:
        sqlite3.Error: Raised if there's an error executing the SQL command.
    """
    cursor = conn.cursor()
    try:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
        conn.commit()
    except sqlite3.Error as e:
        #print(f"An error occurred: {e}")
        pass

def batch_write_to_db(conn, table_name, data_list):
    """
    Insert a batch of data into a specified database table.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite3 database.
        table_name (str): Name of the table to insert data into.
        data_list (list[tuple]): List of tuples with data to insert. Each tuple contains:
            - address (str): Property address.
            - city (str): City of the property.
            - history (str): Serialized string representing property history.
            - status (str): Current property status.
            - statusDate (str): Date of the last status update.
            - dataDate (str): Date of the last data fetch/update.
            - beds (int): Number of bedrooms.
            - baths (int): Number of bathrooms.
            - yearBuilt (int): Year the property was constructed.
            - sqft (int): Property's square footage.

    Raises:
        sqlite3.Error: Raised if there's an error executing the SQL command.
    """
    cursor = conn.cursor()
    try:
        cursor.executemany(f"INSERT OR IGNORE INTO {table_name} (address, city, history, status, statusDate, dataDate, beds, baths, yearBuilt, sqft) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data_list)
        conn.commit()
    except sqlite3.Error as e:
        #print(f"An error occurred: {e}")
        pass

def setup_db(conn, table_name):
    """
    Create a database table with predefined columns if it doesn't exist.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite3 database.
        table_name (str): Name of the table to be created or checked.

    Description:
        If the table does not exist, the function creates it with the following columns:
            - id: Unique auto-incrementing identifier.
            - address: Unique property address.
            - city: City of the property.
            - history: Serialized string of the property's history.
            - status: Current property status.
            - statusDate: Date of the last status update.
            - dataDate: Date of the last data fetch/update.
            - beds: Number of bedrooms.
            - baths: Number of bathrooms.
            - yearBuilt: Year the property was constructed.
            - sqft: Property's square footage.

    Raises:
        sqlite3.Error: Raised if there's an error executing the SQL command.
    """

    cursor = conn.cursor()
    try:
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT UNIQUE,
            city TEXT,
            history TEXT,
            status TEXT,           
            statusDate TEXT,       
            dataDate TEXT,
            beds INTEGER,
            baths INTEGER,
            yearBuilt INTEGER,
            sqft INTEGER
                      
        )
        """)
        conn.commit()
    except sqlite3.Error as e:
        #print(f"An error occurred: {e}")
        pass
    
def addresses_in_db(conn, table_name, addresses):
    """
    Check if a list of addresses already exists in a specified database table.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite3 database.
        table_name (str): Name of the table to check the addresses against.
        addresses (list[str]): List of addresses to check.

    Returns:
        set[str]: A set of addresses found in the database table.
    """
    cursor = conn.cursor()
    placeholders = ', '.join(['?'] * len(addresses))
    cursor.execute(f"SELECT address FROM {table_name} WHERE address IN ({placeholders})", addresses)
    return set(item[0] for item in cursor.fetchall())

def fetch_city_from_db(conn,table_name,city):
    """
    Fetch records from a specified table in the database based on the city name.

    Parameters:
    - conn (sqlite3.Connection): The SQLite database connection object.
    - table_name (str): The name of the table from which to fetch the records.
    - city (str): The name of the city for which to fetch the records.

    Returns:
    - list[tuple]: A list of tuples where each tuple represents a record from the database.
                   The history field in each tuple is deserialized from a JSON string to a Python dictionary.
    """
    cursor = conn.cursor()
    param = (f"%{city}%",)
    cursor.execute(f"SELECT * FROM {table_name} WHERE city LIKE ?", param)
    results = cursor.fetchall()
    deserialized_results = []
    for row in results:
        id, address, city, history_str, status, status_date, data_date, beds, baths, year_built, sqft = row
        # Deserialize the history field
        history = json.loads(history_str)
        deserialized_results.append((id, address, city, history, status, status_date, data_date, beds, baths, year_built, sqft))
    return deserialized_results


def fetch_all_cities_from_db(conn, table_name):
    """
    Fetch records from a specified table in the database for all cities.

    Parameters:
    - conn (sqlite3.Connection): The SQLite database connection object.
    - table_name (str): The name of the table from which to fetch the records.

    Returns:
    - list[tuple]: A list of tuples where each tuple represents a record from the database.
                   The history field in each tuple is deserialized from a JSON string to a Python dictionary.
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    results = cursor.fetchall()
    deserialized_results = []
    for row in results:
        id, address, city, history_str, status, status_date, data_date, beds, baths, year_built, sqft = row
        # Deserialize the history field
        history = json.loads(history_str)
        deserialized_results.append((id, address, city, history, status, status_date, data_date, beds, baths, year_built, sqft))
    return deserialized_results
