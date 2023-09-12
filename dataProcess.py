import asyncio
from getDetails import getDetails
from alive_progress import alive_bar
from geoJsonHelper import read_geojson_features
import concurrent.futures
import json
from databaseHelper import *
import datetime

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
    
    status = data.get('status')
    statusDate = data.get('statusDate')
    dataDate = datetime.datetime.now()
    
    return (address, {'address': address, 'city': props.get('city', 'N/A'), 'history': history_str,'status':status, "statusDate":statusDate,'dataDate':dataDate})

from collector import Redfin
async def process_geojson_data(geojson_file_path,valid_conn,invalid_conn,semaphore,client,batch_size=50):
    geojson_data = read_geojson_features(geojson_file_path)
    valid_data_to_insert = []
    invalid_data_to_insert = []

    all_addresses = [
        f"{feature['properties'].get('number', 'N/A')} {feature['properties'].get('street', 'N/A')}, {feature['properties'].get('city', 'N/A')}, {feature['properties'].get('region', 'N/A')} {feature['properties'].get('postcode', 'N/A')}" 
        for feature in geojson_data[:100000]
    ]
    # Check addresses in batches
    tasks = []
    with alive_bar(len(all_addresses), title='Checking if addresses are in the database') as bar:
        for i in range(0, len(all_addresses), batch_size):
            batch = all_addresses[i:i+batch_size]
            existing_valid_addresses = addresses_in_db(valid_conn, 'validAddress', batch)
            existing_invalid_addresses = addresses_in_db(invalid_conn, 'invalidAddress', batch)
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
                valid_data_to_insert.append((result_data['address'], result_data['city'], result_data['history'],result_data['status'],result_data['statusDate'],result_data['dataDate']))
            else:
                invalid_data_to_insert.append((address, 'N/A', '[]','N/A','N/A','N/A'))
            bar()

    batch_write_to_db(valid_conn, 'validAddress', valid_data_to_insert)
    batch_write_to_db(invalid_conn, 'invalidAddress', invalid_data_to_insert)
    
    

