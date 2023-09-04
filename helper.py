import os
import json

def delete_unwanted_files(path):
    #TODO: some files of states dont have statewide-addresses-state.geojson file
    # will need to adjust the code to see if the file is in the sub folder of the state
    # otherwise search through all files in the subfolder and merged them together to create
    # a statewide-addresses-state.geojson file
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            # can be modified in the future for just city of the state instead
            # reason we want statewide-addresses-state file is because the file
            # contains city values in the json 
            if filename != "statewide-addresses-state.geojson":
                file_to_delete = os.path.join(dirpath, filename)
                try:
                    os.remove(file_to_delete)
                    print(f"Deleted: {file_to_delete}")
                except Exception as e:
                    print(f"Error deleting {file_to_delete}. Error: {e}")

def deleter(folderPath):
    # folder path is the path to files downloaded from openAddresses
    
    if os.path.exists(folderPath) and os.path.isdir(folderPath):
        delete_unwanted_files(folderPath)
        print("Finished deleting unwanted files.")
    else:
        print(f"'{folderPath}' is not a valid directory path.")
        
        
def write_to_file(filename, entry):
    """Append an entry to a file, with each entry on a new line."""
    with open(filename, 'a') as f:  # 'a' mode ensures entries are appended and won't overwrite existing content
        f.write(entry + '\n')  # add a newline after each entry
        
""" 
    This is a temporary place holder for downloading files from https://batch.openaddresses.io/data.
    As of the moment there is issue with using selenium python library to navigate to the URL and download
    the following files us-northeast, us-south, us-midwest, us-west. There may be another method to download the files
    but as of this moment it is not possible
    
"""



def is_valid(entry):
    """
    Check if all required fields are present and non-empty.
    """
    # could add 'region', 'postcode' to required field for better search result from redfin
    required_fields = ['number', 'street', 'city',]
    for field in required_fields:
        if field not in entry['properties'] or not entry['properties'][field]:
            return False
    return True

def remove_duplicates(input_file, output_file):
    # This function cleans up the statewide-addresses-state.geojson file by 
    # 1.) removing duplicate addresses.
    # 2.) removing removing addresses that are from apartments(most likely if the unit field is filed, might also remove false positive addresses)
    # 3.) making sure the addresses from the file have enough fields needed for redfin to find the addresses
    
    # This should help with run time by not wasting time looking for duplicate, apartment, and incomplete addresses.
    unique_entries = set()
    cleaned_data = []

    with open(input_file, 'r') as f:
        for line in f.readlines():
            entry = json.loads(line)
            
            # Skip the entry if not all fields are valid
            if not is_valid(entry):
                continue
            # we dont want address that are from apartments 
            if entry['properties'].get('unit'):
                continue
            
            # reconstruct the address and coordinates
            address = (
                entry['properties']['number'],
                entry['properties']['street'],
                entry['properties']['city'],
                entry['properties']['region'],
                entry['properties']['postcode']
            )
            coords = tuple(entry['geometry']['coordinates'])
            
            unique_key = (address, coords)

            # If this combination has not been encountered before, add it to the set and save the line
            if unique_key not in unique_entries:
                unique_entries.add(unique_key)
                cleaned_data.append(line)

    # Write the cleaned data to the output file
    with open(output_file, 'w') as f:
        for line in cleaned_data:
            f.write(line)


def read_geojson_features(file_path):
    features = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                feature = json.loads(line.strip())
                features.append(feature)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON on line: {line}. Error: {e}")
    return features


