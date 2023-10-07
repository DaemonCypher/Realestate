import datetime
import traceback

async def get_details_closed_property(address,client):
    """
    Fetch details of a closed property based on its address.

    Parameters:
    - address (str): The address to search for.
    - client: An initialized client object to interact with the property service.

    Returns:
    - dict: A dictionary containing the property's details. If an error occurs, an empty string is returned.
    """
    try:
        # Search for property using its address and extract its URL.
        response = await client.search(address)
        url = safe_get(response, 'payload', 'exactMatch', 'url')
        if not url:
            raise ValueError(f"No URL found for address: {address}")
        
        # Extract initial info and propertyId using the URL.
        initial_info = await client.initial_info(url)
        property_id = safe_get(initial_info, 'payload', 'propertyId')
        if not property_id:
            raise ValueError(f"No property ID found for URL: {url}")

        # Extract MLS data and property history.
        mls_data_payload = safe_get(await client.below_the_fold(property_id), 'payload')
        history_payload = safe_get(await client.price_history(property_id), 'payload')

        # Extract the desired data from the payloads.
        event = safe_get(mls_data_payload, 'propertyHistoryInfo', 'events', 0)
        timestamp_seconds = safe_get(event, 'eventDate', default=0) / 1000
        date_obj = datetime.datetime.fromtimestamp(timestamp_seconds)
        home_data =(safe_get(mls_data_payload,'payload','publicRecordsInfo','basicInfo'))
        return {
            'displayedPrice': event.get('price',-1),
            'history': history_payload.get('propertyTimeSeries', []),
            'status': event.get('eventDescription','N/A'),
            'statusDate': date_obj,
            'bed': home_data.get('beds',-1),
            'baths': home_data.get('baths',-1),
            'yearBuilt': home_data.get('yearBuilt',-1),
            'sqft': home_data.get('totalSqFt',-1)
        }

    except ValueError as e:  # For custom error messages
        #print(f"Error encountered: {e}")
        return {}
    except Exception as e:   # For unexpected issues
        #print(f"Unexpected error encountered: {e}")
        #print(traceback.format_exc())
        return {}
  
async def get_details_opened_property(address,client):
    """
    Fetch details of an opened property based on its address.

    Parameters:
    - address (str): The address to search for.
    - client: An initialized client object to interact with the property service.

    Returns:
    - dict: A dictionary containing the property's details. If an error occurs, an empty string is returned.
    """
    try:
        # Search for property using its address and extract its URL.
        response =  await client.search(address)
    
        url = safe_get(response, 'payload', 'exactMatch', 'url')
        if not url:
            raise ValueError(f"No URL found for address: {address}")
      
        # Extract initial info, propertyId, and listingId using the URL.
        initial_info = await client.initial_info(url)
        property_id = safe_get(initial_info, 'payload', 'propertyId')
        if not property_id:
            raise ValueError(f"No property ID found for URL: {url}")
        
        listing_id = safe_get(initial_info, 'payload', 'listingId')
        if not listing_id:
            raise ValueError(f"No listing ID found for URL: {url}")
        
        # Fetch property details using propertyId and listingId.
        property_request= await client.above_the_fold(property_id, listing_id)
        data = safe_get(property_request, 'payload', 'addressSectionInfo')
        price = safe_get(data, 'latestPriceInfo', 'amount', default=-1)
        status = safe_get(data, 'status', 'displayValue', default='N/A')
        sqft = safe_get(data,'sqFt','value', default=-1)
        beds = safe_get(data,'beds', default=-1)
        bath = safe_get(data,'baths', default=-1)
        year_built = safe_get(data,'yearBuilt', default=-1)
        # Fetch property price history.
        price_history = await client.avm_historical(property_id, listing_id)
        status_date = safe_get(price_history, 'payload', 'avmUpdateDate', default=0) / 1000
        date_obj = datetime.datetime.fromtimestamp(status_date)
        history = safe_get(price_history, 'payload', 'propertyTimeSeries', default=[])

        return{
            'displayedPrice': price,
            'history': history,
            'status': status,
            'statusDate': date_obj,
            'bed': beds,
            'baths': bath,
            'yearBuilt': year_built,
            'sqft': sqft
        }

    except ValueError as e:  # For custom error messages
        #print(f"Error encountered: {e}")
        return {}
    except Exception as e:   # For unexpected issues
        #print(f"Unexpected error encountered: {e}")
        #print(traceback.format_exc())
        return {}
    
def safe_get(data, *keys, default=None):
    """
    Safely retrieve a value from a nested dictionary or list.
    
    Parameters:
    - data (dict/list): The dictionary or list to navigate.
    - keys: A series of keys/indices to retrieve the desired value.
    - default: The value to return if the desired value is not found. Defaults to None.

    Returns:
    - The desired value if found, else the default value.
    """
    for key in keys:
        if isinstance(data, list) and isinstance(key, int):
            # If data is a list and key is an index, check if index is within bounds.
            if key < len(data):
                data = data[key]
            else:
                return default
        else:
            try:
                data = data[key]
            except (KeyError, TypeError):
                return default
    return data

async def get_details(address, client):
    """
    Fetch details of a property. Prioritizes closed properties over opened ones for efficiency reasons.

    Parameters:
    - address (str): The address to search for.
    - client: An initialized client object to interact with the property service.

    Returns:
    - dict: A dictionary containing the property's details. If an error occurs, an empty string is returned.
    """

    open_property = await get_details_opened_property(address, client)
    if open_property != "":
        return open_property

    close_property = await get_details_closed_property(address,client)
    if close_property != "":
        return close_property
    

    return {}
