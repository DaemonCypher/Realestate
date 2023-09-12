import sqlite3
import json 

def fetch_specific_from_db(conn,table_name,column):
    """ 
    Grabs all values from a specific column in a given table from the database.

    Args:
        conn (sqlite3.Connection): The SQLite3 connection object to the database.
        table_name (str): The name of the table from which data needs to be fetched.
        column (str): The name of the column whose values are to be fetched.

    Returns:
        list[tuple]: A list of tuples where each tuple contains a value from the specified column.
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT {column} FROM {table_name}")
    results = cursor.fetchall()
    return results

def fetch_from_db(conn, table_name):
    """
    Grabs all values from a given table from the database.

    Args:
        conn (sqlite3.Connection): The SQLite3 connection object to the database.
        table_name (str): The name of the table from which data needs to be fetched.

    Returns:
        list[tuple]: A list of tuples containing all value from the specified table.
        Each tuple contains:
            - id (int): A unique identifier for each record.
            - address (str): The address value.
            - city (str): The city value.
            - history (list): A list containing the history data.
            - status (str): The status value.
            - statusDate (str): The status date value.
            - dataDate (str): The data date value.
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, address, city, history, status, statusDate, dataDate FROM {table_name}")
    results = cursor.fetchall()

    deserialized_results = []
    for row in results:
        id,address, city, history_str,status,statusDate,dataDate = row
        # Deserialize the history field
        history = json.loads(history_str)
        deserialized_results.append((id, address, city, history,status,statusDate,dataDate))
    return deserialized_results

def add_column_to_table(conn, table_name, column_name, column_type):
    """
    Adds a new column to a specified table in the database.

    Args:
        conn (sqlite3.Connection): The SQLite3 connection object to the database.
        table_name (str): The name of the table from which data needs to be fetched.
        column_name (str): The name of the column whose values are to be fetched.
        column_type (str): The data type of the new column (e.g., 'TEXT', 'INTEGER', 'REAL', etc.).
    Raises:
        sqlite3.Error: If there's an issue executing the SQL command.
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
    Writes a batch of data to a specified table in the database.

    Args:
        conn (sqlite3.Connection): The SQLite3 connection object to the database.
        table_name (str): The name of the table where the data needs to be inserted.
        data_list (list[tuple]): A list of tuples containing data to be inserted. Each tuple should have the following structure:
            - address (str): The address of the property.
            - city (str): The city where the property is located.
            - history (str): A serialized string representing the history of the property.
            - status (str): The current status of the property.
            - statusDate (str): The date when the status was last updated.
            - dataDate (str): The date when the data was last fetched or updated.

    Raises:
        sqlite3.Error: If there's an issue executing the SQL command.
    """
    cursor = conn.cursor()
    try:
        cursor.executemany(f"INSERT OR IGNORE INTO {table_name} (address, city, history, status, statusDate, dataDate) VALUES (?, ?, ?, ?, ?, ?)", data_list)
        conn.commit()
    except sqlite3.Error as e:
        #print(f"An error occurred: {e}")
        pass

def setup_db(conn, table_name):
    """
    Sets up a database table with predefined columns if it doesn't already exist.

    Args:
        conn (sqlite3.Connection): The SQLite3 connection object to the database.
        table_name (str): The name of the table to be created or verified.

    Description:
        The function creates a table with the following columns:
            - id (INTEGER): A unique identifier for each record. It auto-increments with each new entry.
            - address (TEXT): The address of the property. It is unique to ensure no duplicate addresses are stored.
            - city (TEXT): The city where the property is located.
            - history (TEXT): A serialized string representing the history of the property.
            - status (TEXT): The current status of the property.
            - statusDate (TEXT): The date when the status was last updated.
            - dataDate (TEXT): The date when the data was last fetched or updated.

    Raises:
        sqlite3.Error: If there's an issue executing the SQL command.
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
            dataDate TEXT          
        )
        """)
        conn.commit()
    except sqlite3.Error as e:
        #print(f"An error occurred: {e}")
        pass

def addresses_in_db(conn, table_name, addresses):
    """
    Grabs addresses from the database that match the provided list of addresses.

    Args:
        conn (sqlite3.Connection): The SQLite3 connection object to the database.
        table_name (str): The name of the table to fetch the addresses from.
        addresses (list[str]): A list of address strings to check against the database.

    Returns:
        set[str]: A set containing addresses that were found in the database.
    """
    cursor = conn.cursor()
    placeholders = ', '.join(['?'] * len(addresses))
    cursor.execute(f"SELECT address FROM {table_name} WHERE address IN ({placeholders})", addresses)
    return set(item[0] for item in cursor.fetchall())
