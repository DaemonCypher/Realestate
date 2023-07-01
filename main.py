from getDetails import *
from getAdresses import *
import os 
import json


data = getDetails("155 BATTERY PARK DR")


num_beds = data['payload']['numBeds']
num_baths = data['payload']['numBaths']
sq_ft = data['payload']['sqFt']['value']
listing_price = data['payload']['listingPrice']
is_serviced = data['payload']['isServiced']
is_active = data['payload']['isActivish']
latitude = data['payload']['latLong']['latitude']
longitude = data['payload']['latLong']['longitude']
price_amount = data['payload']['priceInfo']['amount']
assembled_address = data['payload']['streetAddress']['assembledAddress']
predicted_value = data['payload']['predictedValue']

# Print the extracted information
print(f"Number of Beds: {num_beds}")
print(f"Number of Baths: {num_baths}")
print(f"Square Feet: {sq_ft}")
print(f"Listing Price: {listing_price}")
print(f"Is Serviced: {is_serviced}")
print(f"Is Active: {is_active}")
print(f"Latitude: {latitude}")
print(f"Longitude: {longitude}")
print(f"Price Amount: {price_amount}")
print(f"Assembled Address: {assembled_address}")
print(f"Predicted Value: {predicted_value}")