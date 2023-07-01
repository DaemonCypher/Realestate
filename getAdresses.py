import geopandas as gpd

def getAddress(file):
    data = gpd.read_file(file)
    address = {}
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
    return address