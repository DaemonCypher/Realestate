import asyncio
from getDetails import getDetails
from alive_progress import alive_bar
from helper import read_geojson_features
import concurrent.futures
from collector import Redfin
import sqlite3
client = Redfin()
semaphore = asyncio.Semaphore(250)


valid_conn  = sqlite3.connect("validAddress.db")
invalid_conn = sqlite3.connect("invalidAddress.db")

def setup_db(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT,
        city TEXT,
        history TEXT
    )
    """)
    conn.commit()

setup_db(valid_conn, "valid_addresses")
setup_db(invalid_conn, "invalid_addresses")

def _batch_write_to_db(conn, table_name, data_list):
    cursor = conn.cursor()
    cursor.executemany(f"INSERT INTO {table_name} (address, city, history) VALUES (?, ?, ?)", data_list)
    conn.commit()

async def process_feature_with_limit(feature, semaphore, client):
    async with semaphore:
        return await process_feature(feature, client)


async def process_feature(feature, client):
    props = feature.get("properties", {})

    address = f"{props.get('number', 'N/A')} {props.get('street', 'N/A')}, {props.get('city', 'N/A')}, {props.get('region', 'N/A')} {props.get('postcode', 'N/A')}"
    data = await getDetails(address, client)

    if not data or data == "":
        return (address, None)

    history = data.get('history', [])
    if not isinstance(history, list):
        history = []

    # current price shown on redfin    
    #displayed_price = data.get('displayedPrice', 'N/A')
    # current status shown on redfin
    #status = data.get('status', 'N/A')
    # date of current status shown on redfin
    #status_date = data['statusDate'].strftime('%Y-%m-%d %H:%M:%S') if data.get('statusDate') else "N/A"
    # redfin estimated price history on redfin
    
    return (address, {'city': props.get('city', 'N/A'), 'history': history})


async def process_geojson_data(geojson_file_path):
    geojson_data = read_geojson_features(geojson_file_path)
    data = []
    invalid_addresses = []
    valid_addresses = []

    tasks = [process_feature_with_limit(feature, semaphore, client) for feature in geojson_data[:10000]]

    with alive_bar(len(tasks), title='Processing addresses') as bar:
        for future in asyncio.as_completed(tasks):
            address, result_data = await future

            if result_data and result_data['city'] and result_data['history']:
                data.append((result_data['city'], result_data['history']))
                valid_addresses.append(address)
            else:
                invalid_addresses.append(address)

            bar()

    _batch_write_to_file("nonResidental.txt", invalid_addresses)
    _batch_write_to_file("residential.txt", valid_addresses)

    return data


def _batch_write_to_file(filename, data_list, batch_size=100):
    with open(filename, "a") as f:
        for i in range(0, len(data_list), batch_size):
            batch = data_list[i:i+batch_size]
            f.write('\n'.join(batch) + '\n')


# Running the asynchronous function
data = asyncio.run(process_geojson_data('file path'))


async def process_feature_with_limit(feature, semaphore, client):
    async with semaphore:
        return await process_feature(feature, client)


async def process_feature(feature, client):
    props = feature.get("properties", {})

    address = f"{props.get('number', 'N/A')} {props.get('street', 'N/A')}, {props.get('city', 'N/A')}, {props.get('region', 'N/A')} {props.get('postcode', 'N/A')}"
    data = await getDetails(address, client)

    if not data or data == "":
        return (address, None)

    history = data.get('history', [])
    if not isinstance(history, list):
        history = []

    # current price shown on redfin    
    #displayed_price = data.get('displayedPrice', 'N/A')
    # current status shown on redfin
    #status = data.get('status', 'N/A')
    # date of current status shown on redfin
    #status_date = data['statusDate'].strftime('%Y-%m-%d %H:%M:%S') if data.get('statusDate') else "N/A"
    # redfin estimated price history on redfin
    
    return (address, {'city': props.get('city', 'N/A'), 'history': history})


async def process_geojson_data(geojson_file_path):
    geojson_data = read_geojson_features(geojson_file_path)
    data = []
    invalid_addresses = []
    valid_addresses = []

    tasks = [process_feature_with_limit(feature, semaphore, client) for feature in geojson_data[:10000]]

    with alive_bar(len(tasks), title='Processing addresses') as bar:
        for future in asyncio.as_completed(tasks):
            address, result_data = await future

            if result_data and result_data['city'] and result_data['history']:
                _batch_write_to_db(valid_conn, "valid_addresses", [(address, result_data['city'], str(result_data['history']))])
            else:
                _batch_write_to_db(invalid_conn, "invalid_addresses", [(address, "N/A", "N/A")])

            bar()

    return data


def _batch_write_to_file(filename, data_list, batch_size=100):
    with open(filename, "a") as f:
        for i in range(0, len(data_list), batch_size):
            batch = data_list[i:i+batch_size]
            f.write('\n'.join(batch) + '\n')


# Running the asynchronous function
data = asyncio.run(process_geojson_data('file path'))
valid_conn.close()
invalid_conn.close()
