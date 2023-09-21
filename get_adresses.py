import geopandas as gpd
from tqdm import tqdm

def get_address(file):
    """
    Parse and format addresses from a .geojson file.

    The function reads address details from the given .geojson file and structures 
    them in a readable format. This can be used to develop price history for various 
    geographical entities like cities, counties, or states. The resultant address 
    dictionary can be used for quick access and updates regarding average price 
    changes in these areas.

    Parameters:
    - file (str): Path to the .geojson file containing address data.

    Returns:
    - dict: Dictionary with keys being the index and values being the formatted address.
    """

    print("Reading addresses from the file...")
    data = gpd.read_file(file)
    address = {}  # Dictionary to store formatted addresses.

    # Use tqdm to indicate processing progress for each address entry.
    for index, row in tqdm(data.iterrows(), total=len(data), desc='Processing Addresses'):
        # Extract address components.
        number = row['number']
        street = row['street']
        unit = row['unit']
        city = row['city']
        district = row['district'] # county
        region = row['region']     # state
        postcode = row['postcode']

        # Initialize empty string for address formatting.
        output = ""

        # Concatenate available address components.
        if number:
            output += number + " "
        if street:
            output += street + " "
        if unit:
            output += unit + ", " 
        if city:
            output += city + ", " 
        if district:
            output += district + ", "
        if region:
            output += region + " "
        if postcode:
            output += postcode

        # Add the formatted address to the dictionary.
        address[index] = output

    return address
