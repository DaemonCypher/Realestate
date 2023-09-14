import os
import json


def delete_unwanted_files(path):
    """
    Deletes all files in the given directory tree, except for "statewide-addresses-state.geojson".
    
    If the desired file doesn't exist in a subfolder, consider merging other files to create one.
    (Note: The merging functionality is not provided here; a placeholder comment is used instead.)
    """
    
    # Flag to check if the desired file exists in the current directory
    has_statewide_file = False
    
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename == "statewide-addresses-state.geojson":
                has_statewide_file = True
            else:
                # Delete the file if it's not the desired file
                file_to_delete = os.path.join(dirpath, filename)
                try:
                    os.remove(file_to_delete)
                    print(f"Deleted: {file_to_delete}")
                except Exception as e:
                    print(f"Error deleting {file_to_delete}. Error: {e}")
                    
        # Placeholder: Merge functionality can be added here if `has_statewide_file` is False.
        if not has_statewide_file:
            print(f"No 'statewide-addresses-state.geojson' in {dirpath}. Consider merging other files.")
        has_statewide_file = False  # Reset the flag for the next directory
        
def deleter():
    curdir =os.getcwd()
    folderPath = os.path.join(curdir,"downloads")
    # folder path is the path to files downloaded from openAddresses
    if os.path.exists(folderPath) and os.path.isdir(folderPath):
        delete_unwanted_files(folderPath)
        print("Finished deleting unwanted files.")
    else:
        print(f"'{folderPath}' is not a valid directory path.") 
      
""" 
    This is a temporary place holder for downloading files from https://batch.openaddresses.io/data.
    As of the moment there is issue with using selenium python library to navigate to the URL and download
    the following files us-northeast, us-south, us-midwest, us-west. There may be another method to download the files
    but as of this moment it is not possible.
    Might be better to have the user download the files themselves and drop it into downloads
    
"""

def find_file(root_path, target_file):
    for dirpath, dirnames, filenames in os.walk(root_path):
        if target_file in filenames:
            return os.path.join(dirpath, target_file)
    return None

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

def find_state_folder(root_path, state):
    """
    This function will search through all subdirectories in the root path until
    it finds a directory that matches the state name.
    """
    for dirpath, dirnames, _ in os.walk(root_path):
        if state in dirnames:
            return os.path.join(dirpath, state)
    return None

def remove_duplicates(state):
    # This function cleans up the statewide-addresses-state.geojson file by 
    # 1.) removing duplicate addresses.
    # 2.) removing removing addresses that are from apartments(most likely if the unit field is filed, might also remove false positive addresses)
    # 3.) making sure the addresses from the file have enough fields needed for redfin to find the addresses
    
    # This should help with run time by not wasting time looking for duplicate, apartment, and incomplete addresses.
    state = state.lower()
    target_file = "statewide-addresses-state.geojson"
    curdir = os.getcwd()
    output_path = os.path.join(curdir, "cleaned")
    input_path = os.path.join(curdir, "downloads")
    
    state_folder = find_state_folder(input_path, state)
    if not state_folder:
        print(f"Folder for {state} not found!")
        return None
    
    path = find_file(state_folder, target_file)
    if path == None:
        print(f"{target_file} not found in {state} folder!")
        return None
    
    unique_entries = set()
    cleaned_data = []

    with open(path, 'r') as f:
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
    os.chdir(output_path)
    output_file = state + ".geojson"
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
