
import datetime
import traceback


#TODO: there is a bug with client.search where there is no url to the address provided
async def getDetails(address,client):
    try:
        # Search for property and get the URL
        response = await client.search(address)
        url = response.get('payload', {}).get('exactMatch', {}).get('url')
        if not url:
            raise ValueError(f"No URL found for address: {address}")

        # Get initial info and propertyId
        initial_info = await client.initial_info(url)
        property_id = initial_info.get('payload', {}).get('propertyId')
        if not property_id:
            raise ValueError(f"No property ID found for URL: {url}")

        # Fetch MLS data and history
        mls_data_payload = (await client.below_the_fold(property_id)).get('payload', {})
        history_payload = (await client.price_history(property_id)).get('payload', {})

        # Extract necessary data
        event = mls_data_payload.get('propertyHistoryInfo', {}).get('events', [{}])[0]
        timestamp_seconds = event.get('eventDate', 0) / 1000
        date_obj = datetime.datetime.fromtimestamp(timestamp_seconds)

        return {
            'displayedPrice': event.get('price'),
            'history': history_payload.get('propertyTimeSeries', []),
            'status': event.get('eventDescription'),
            'statusDate': date_obj
        }
        
 
        
    
        # can get info from mls_data
        #listing_id = initial_info['payload']['listingId']
        #property_request=client.above_the_fold(property_id,listing_id)
        # can get data from above_the_fold
        
        #avm_details = client.avm_details(property_id, listing_id)
        #price_history= client.avm_historical(property_id, listing_id)
        #each index in history is 1 month and combined to be last 5 years
        # so current month and going back as far as possible in the last 5 years
        #history = price_history['payload']['propertyTimeSeries']
        #last_update = price_history['payload']['avmUpdateDate']

        #data =({'mls_data':mls_data},{'property_request':property_request},{'avm_details':avm_details},{'price_history':price_history})
    except ValueError as e:  # Catches the custom error messages
        #print(f"Error encountered: {e}")
        return ""
    except Exception as e:  # Catches unexpected issues
        #print(f"Unexpected error encountered: {e}")
        #print(traceback.format_exc())
        return ""

    return ""  # This will be returned if the function hasn't returned until this point

def safe_get(data, *keys):
    """
    Safely retrieve a value from a nested dictionary.
    
    Parameters:
    - data: The dictionary to search.
    - keys: A series of keys to navigate through the dictionary.
    - default: The value to return if any key is not found. Defaults to None.
    
    Returns:
    - The found value or the default value.
    """
    for key in keys:
        if isinstance(data, list) and isinstance(key, int):
            # If data is a list and key is an index, check if index is within bounds.
            if key < len(data):
                data = data[key]
            else:
                return None
        else:
            try:
                data = data[key]
            except (KeyError, TypeError):
                return None
    return data