import geopandas as gpd
from alive_progress import alive_bar

def getAddress(file):
    # Reads details from the .geojson file and appends them to a dictionary
    # for the future when developing an price history of a city,county,state
    # will use the dictionary file for quick access of seeing the price change
    # and updating the average price of an area
    
    
    with alive_bar(title='Reading addresses from the file...') as loading:
        data = gpd.read_file(file)
        address = {}
        loading()
    
    with alive_bar(len(data), title='Processing Addresses',) as bar:
        for index, row in data.iterrows():
            number = row['number']
            street = row['street']
            unit = row['unit']
            city = row['city']
            district = row['district'] # county
            region = row['region'] # state
            postcode = row['postcode']
            output = ""
            if number:
                output = output + number + " "
            if street:
                output = output + street + " "
            if unit:
                output =output + unit + ", " 
            if city:
                output = output + city + ", " 
            if district:
                output = output + district + ", "
            if region:
                output = output + region + " "
            if postcode:
                output = output + postcode
            address[index] = output
            
            # Each time the loop iterates, update the progress bar.
            bar()
    return address
