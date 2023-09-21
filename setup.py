from collector import Redfin
import asyncio
from data_process import process_geojson_data
import os
import argparse
from geo_json_helper import *
from database_helper import *

def initial():
    """
    Parse command-line arguments to obtain state, number of addresses to collect, and an optional cleanup flag.
    
    Returns:
        argparse.Namespace: Parsed arguments from the command line.
    """
    parser = argparse.ArgumentParser(description="Accept an integer and a name from the command line.")
    parser.add_argument('-i', '--integer', type=int, required=True, help="How many Addresses to collect")
    parser.add_argument('-n', '--name', type=str, required=True, help="State to look at")
    parser.add_argument("-f", "--flag", action="store_true", help="Flag to clean up files")
    args = parser.parse_args()
    return args

def setup():
    """
    Set up the environment and process geojson data for addresses.
    
    This function does the following:
    1.) Parses command-line arguments.
    2.) Optionally cleans up existing files.
    3.) Sets up the Redfin client.
    4.) Initializes SQLite databases for valid and invalid addresses.
    5.) Processes the geojson data, extracting and storing address details in databases.
    6.) Closes the database connections.
    """
    # Get the current working directory
    root_dir = os.getcwd()
    
    # Parse command-line arguments
    args = initial()
    state_name = args.name.lower()
    file = state_name + ".geojson"
    
    # Perform cleanup if flag is set
    if args.flag:
        deleter()
        remove_duplicates(state_name)
    os.chdir(root_dir)
    
    # Initialize Redfin client and setup concurrency control
    client = Redfin()
    semaphore = asyncio.Semaphore(250)
    
    # Connect to SQLite databases
    valid_conn = sqlite3.connect("validAddress.db")
    invalid_conn = sqlite3.connect("invalidAddress.db")
    
    # Setup tables in databases
    setup_db(valid_conn, "validAddress")
    setup_db(invalid_conn, "invalidAddress")
    
    # Construct the path for the cleaned geojson file and process it
    file_path = os.path.join(root_dir, "cleaned", file)
    asyncio.run(process_geojson_data(file_path, valid_conn, invalid_conn, semaphore, client, args.integer))
    
    # Close the database connections
    valid_conn.close()
    invalid_conn.close()

if __name__ == "__main__":
    # Execute the setup function when this script is run directly
    setup()
