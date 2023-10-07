import asyncio
from get_details import get_details
from geo_json_helper import read_geojson_features
import concurrent.futures
import json
from database_helper import addresses_in_db, batch_write_to_db
import datetime
from tqdm import tqdm

async def process_feature_with_limit(feature, semaphore, client):
    """
    Process a feature while limiting concurrency using a semaphore.
    
    Args:
        feature (dict): The geojson feature to be processed.
        semaphore (asyncio.Semaphore): A semaphore to limit the number of concurrent tasks.
        client: Redfin class 

    Returns:
        tuple: A tuple containing address details.
    """
    async with semaphore:
        return await process_feature(feature, client)

async def process_feature(feature, client):
    """
    Process the provided geojson feature to extract address details.
    
    Args:
        feature (dict): The geojson feature to be processed.
        client: RedFin Class.

    Returns:
        tuple: A tuple containing the address and its details (or None if data extraction fails).
    """
    
    # Construct the address string from feature properties
    props = feature.get("properties", {})
    address = f"{props.get('number', 'N/A')} {props.get('street', 'N/A')}, {props.get('city', 'N/A')}, {props.get('region', 'N/A')} {props.get('postcode', 'N/A')}"

    # Retrieve address details
    data = await get_details(address, client)
    if not data or data == {}:
        return (address, None)

    # Extract history, status, and relevant dates
    history = data.get('history', [])
    history_str = json.dumps(history) if isinstance(history, list) else '[]'
    
    status = data.get('status')
    status_date = data.get('statusDate')
    data_date = datetime.datetime.now()
    bed = data.get('bed')
    baths = data.get('baths')
    year_built = data.get('yearBuilt')
    sqft = data.get('sqft')
    
    # Return processed data in desired format
    return (address, {
        'address': address, 
        'city': props.get('city', 'N/A'), 
        'history': history_str, 
        'status': status, 
        'statusDate': status_date, 
        'dataDate': data_date, 
        'beds': bed, 
        'baths': baths,
        'yearBuilt': year_built, 
        'sqft':sqft})

async def process_geojson_data(geojson_file_path, valid_conn, invalid_conn, semaphore, client, size, batch_size=50):
    """
    Process the data from a geojson file and save the results in the database.
    
    Args:
        geojson_file_path (str): Path to the .geojson file.
        valid_conn (sqlite3.Connection): Database connection for valid addresses.
        invalid_conn (sqlite3.Connection): Database connection for invalid addresses.
        semaphore (asyncio.Semaphore): A semaphore to limit concurrency.
        client: Redfin Class.
        size (int): Number of geojson features to process.
        batch_size (int, optional): Size of address batches to check in the database. Defaults to 50.
    """
    
    geojson_data = read_geojson_features(geojson_file_path)
    valid_data_to_insert = []
    invalid_data_to_insert = []

    # Generate a list of all address strings
    all_addresses = [
        f"{feature['properties'].get('number', 'N/A')} {feature['properties'].get('street', 'N/A')}, {feature['properties'].get('city', 'N/A')}, {feature['properties'].get('region', 'N/A')} {feature['properties'].get('postcode', 'N/A')}" 
        for feature in geojson_data[:size]
    ]
    
    tasks = []

    # Iterate over the address list in batches
    for i in tqdm(range(0, len(all_addresses), batch_size), desc='Checking if addresses are in the database'):
        batch = all_addresses[i:i+batch_size]
        
        # Check if addresses are already in the database
        existing_valid_addresses = addresses_in_db(valid_conn, 'validAddress', batch)
        existing_invalid_addresses = addresses_in_db(invalid_conn, 'invalidAddress', batch)
        
        for feature in geojson_data[i:i+batch_size]:
            props = feature.get("properties", {})
            address = f"{props.get('number', 'N/A')} {props.get('street', 'N/A')}, {props.get('city', 'N/A')}, {props.get('region', 'N/A')} {props.get('postcode', 'N/A')}"
            
            # Only process addresses that aren't already in the databases
            if address not in existing_valid_addresses and address not in existing_invalid_addresses:
                tasks.append(process_feature_with_limit(feature, semaphore, client))

    # Process tasks asynchronously and gather results
    for future in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc='Processing addresses'):
        address, result_data = await future
        if result_data:
            valid_data_to_insert.append((result_data['address'], 
                                         result_data['city'], 
                                         result_data['history'], 
                                         result_data['status'], 
                                         result_data['statusDate'], 
                                         result_data['dataDate'], 
                                         result_data['beds'], 
                                         result_data['baths'], 
                                         result_data['yearBuilt'], 
                                         result_data['sqft']))
        else:
            invalid_data_to_insert.append((address, 'N/A', '[]', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'))
          
    # Write the processed data to the database
    batch_write_to_db(valid_conn, 'validAddress', valid_data_to_insert)
    batch_write_to_db(invalid_conn, 'invalidAddress', invalid_data_to_insert)
