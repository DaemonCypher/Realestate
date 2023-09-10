import asyncio
from getDetails import getDetails
from alive_progress import alive_bar
from helper import read_geojson_features
import concurrent.futures
from collector import Redfin
import sqlite3
import json

client = Redfin()
semaphore = asyncio.Semaphore(250)

valid_conn  = sqlite3.connect("validAddress.db")
invalid_conn = sqlite3.connect("invalidAddress.db")

def setup_db(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT UNIQUE,
        city TEXT,
        history TEXT
    )
    """)
    conn.commit()

setup_db(valid_conn, "valid_addresses")
setup_db(invalid_conn, "invalid_addresses")

def _batch_write_to_db(conn, table_name, data_list):
    cursor = conn.cursor()
    cursor.executemany(f"INSERT OR IGNORE INTO {table_name} (address, city, history) VALUES (?, ?, ?)", data_list)
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
    history_str = json.dumps(history) if isinstance(history, list) else '[]'
    return (address, {'address': address, 'city': props.get('city', 'N/A'), 'history': history_str})

def addresses_in_db(conn, table_name, addresses):
    cursor = conn.cursor()
    placeholders = ', '.join(['?'] * len(addresses))
    cursor.execute(f"SELECT address FROM {table_name} WHERE address IN ({placeholders})", addresses)
    return set(item[0] for item in cursor.fetchall())

async def process_geojson_data(geojson_file_path, batch_size=50):
    geojson_data = read_geojson_features(geojson_file_path)
    valid_data_to_insert = []
    invalid_data_to_insert = []

    all_addresses = [
        f"{feature['properties'].get('number', 'N/A')} {feature['properties'].get('street', 'N/A')}, {feature['properties'].get('city', 'N/A')}, {feature['properties'].get('region', 'N/A')} {feature['properties'].get('postcode', 'N/A')}" 
        for feature in geojson_data[:200000]
    ]
    
    # Check addresses in batches
    tasks = []
    with alive_bar(len(all_addresses), title='Checking if addresses are in the database') as bar:
        for i in range(0, len(all_addresses), batch_size):
            batch = all_addresses[i:i+batch_size]
            existing_valid_addresses = addresses_in_db(valid_conn, 'valid_addresses', batch)
            existing_invalid_addresses = addresses_in_db(invalid_conn, 'invalid_addresses', batch)
            for feature in geojson_data[i:i+batch_size]:
                props = feature.get("properties", {})
                address = f"{props.get('number', 'N/A')} {props.get('street', 'N/A')}, {props.get('city', 'N/A')}, {props.get('region', 'N/A')} {props.get('postcode', 'N/A')}"
                if address not in existing_valid_addresses and address not in existing_invalid_addresses:
                    tasks.append(process_feature_with_limit(feature, semaphore, client))
                bar()

    with alive_bar(len(tasks), title='Processing addresses') as bar:
        for future in asyncio.as_completed(tasks):
            address, result_data = await future
            if result_data:
                valid_data_to_insert.append((result_data['address'], result_data['city'], result_data['history']))
            else:
                invalid_data_to_insert.append((address, 'N/A', '[]'))
            bar()

    _batch_write_to_db(valid_conn, 'valid_addresses', valid_data_to_insert)
    _batch_write_to_db(invalid_conn, 'invalid_addresses', invalid_data_to_insert)
    return valid_data_to_insert

# Running the asynchronous function
data = asyncio.run(process_geojson_data(r'C:\Users\willi\Desktop\Realestate\cleaned.geojson'))


valid_conn.close()
invalid_conn.close()
