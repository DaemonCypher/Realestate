import geopandas as gpd
from alive_progress import alive_bar

def getAddress(file):
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

    # Use a progress bar to indicate reading progress.
    with alive_bar(title='Reading addresses from the file...') as loading:
        data = gpd.read_file(file)
        address = {}  # Dictionary to store formatted addresses.
        loading()  # Update the loading bar.

    # Use a progress bar to indicate processing progress for each address entry.
    with alive_bar(len(data), title='Processing Addresses') as bar:
        for index, row in data.iterrows():
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

            # Update the progress bar.
            bar()

    return address
