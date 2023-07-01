from redfin import Redfin

client = Redfin()

def getDetails(address):
    # if redfin can find the data return all values else return ""
    try:
        response = client.search(address)
        url = response['payload']['exactMatch']['url']
        initial_info = client.initial_info(url)

        property_id = initial_info['payload']['propertyId']
        mls_data = client.below_the_fold(property_id)

        listing_id = initial_info['payload']['listingId']
        avm_details = client.avm_details(property_id, listing_id)
        return avm_details
    except:
        return ""
