import os
import json
import glob

def is_valid_format(line):
    """Checks if a line conforms to the specified JSON format."""
    try:
        entry = json.loads(line)
    except json.JSONDecodeError:
        return False

    # Check top-level keys
    if set(entry.keys()) != {"type", "properties", "geometry"}:
        return False
    
    # Check properties keys
    if set(entry["properties"].keys()) != {"hash", "number", "street", "unit", "city", "district", "region", "postcode", "id"}:
        return False
    
    # Check geometry keys
    if set(entry["geometry"].keys()) != {"type", "coordinates"}:
        return False
    
    return True

def merge_files(dirpath, output_file_path):
    """
    Merges content from multiple .geojson files into a single file within a specified directory.

    Parameters:
    dirpath (str): Path of the directory containing .geojson files to merge.
    output_file_path (str): Path of the file to write merged content to.
    """
    # Get all .geojson files in the specified directory
    file_paths = glob.glob(os.path.join(dirpath, '*.geojson'))
    with open(output_file_path, 'w') as output_file:
        for file_path in file_paths:
            with open(file_path, 'r') as input_file:
                for line in input_file:
                    if is_valid_format(line):
                        output_file.write(line)

def delete_unwanted_files(path):
    """
    Deletes all files in the given directory tree, except for "statewide-addresses-state.geojson".
    
    If the desired file doesn't exist in a subfolder, the function suggests merging other files 
    to create the desired one.
    """
    
    # Walking through the directory tree rooted at path
    for dirpath, dirnames, filenames in os.walk(path):
        
        # If the desired file doesn't exist, it suggests merging other files.
        if "statewide-addresses-state.geojson" not in filenames:
            print(f"No 'statewide-addresses-state.geojson' in {dirpath}. Merging other files.")
            output_file_path = os.path.join(dirpath, 'statewide-addresses-state.geojson')
            merge_files(dirpath, output_file_path)
        
        # Iterate through the files and delete those that are not the desired file
        for filename in filenames:
            if filename != "statewide-addresses-state.geojson":
                # Delete the file if it's not the desired file
                file_to_delete = os.path.join(dirpath, filename)
                try:
                    os.remove(file_to_delete)
                    print(f"Deleted: {file_to_delete}")
                except Exception as e:
                    print(f"Error deleting {file_to_delete}. Error: {e}")
           
def deleter():
    """
    Deletes unwanted files in the 'downloads' folder.
    
    Assumes the 'downloads' folder is present in the current working directory.
    """
    cur_dir = os.getcwd()
    folder_path = os.path.join(cur_dir, "downloads")
    
    # If the directory exists, invoke the delete_unwanted_files function.
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        delete_unwanted_files(folder_path)
        print("Finished deleting unwanted files.")
    else:
        print(f"'{folder_path}' is not a valid directory path.") 

def find_file(root_path, target_file):
    """
    Searches for a target file in a given root directory.
    
    Args:
        root_path (str): Directory to start the search from.
        target_file (str): Name of the file to search for.
        
    Returns:
        str: Path to the target file if found, else None.
    """
    for dir_path, dir_names, filenames in os.walk(root_path):
        if target_file in filenames:
            return os.path.join(dir_path, target_file)
    return None

def is_valid(entry):
    """
    Validates if all required fields are present and non-empty in the entry.
    
    Args:
        entry (dict): Entry with fields to validate.
    
    Returns:
        bool: True if all required fields are present and non-empty, else False.
    """
    required_fields = ['number', 'street', 'city']
    for field in required_fields:
        if field not in entry['properties'] or not entry['properties'][field]:
            return False
    return True

def find_state_folder(root_path, state):
    """
    Searches for a subdirectory matching the state name in a given root directory.
    
    Args:
        root_path (str): Directory to start the search from.
        state (str): Name of the state to search for.
        
    Returns:
        str: Path to the state directory if found, else None.
    """
    for dirpath, dirnames, _ in os.walk(root_path):
        if state in dirnames:
            return os.path.join(dirpath, state)
    return None

def remove_duplicates(state):
    """
    Cleans up the "statewide-addresses-state.geojson" file by performing the following actions:
    1.) Removing duplicate addresses.
    2.) Excluding addresses from apartments (assumption: if 'unit' field is filled, it's an apartment).
    3.) Ensuring addresses have the necessary fields for Redfin.
    
    Args:
        state (str): The state name where the corresponding .geojson file resides.

    Returns:
        None
    """
    state = state.lower()
    target_file = "statewide-addresses-state.geojson"
    cur_dir = os.getcwd()
    output_path = os.path.join(cur_dir, "cleaned")
    input_path = os.path.join(cur_dir, "downloads")
    
    state_folder = find_state_folder(input_path, state)
    
    # Check if the folder for the given state exists
    if not state_folder:
        print(f"Folder for {state} not found!")
        return None
    
    path = find_file(state_folder, target_file)
    
    # Check if the specified geojson file exists within the state folder
    if path == None:
        print(f"{target_file} not found in {state} folder!")
        return None
    
    unique_entries = set()
    cleaned_data = []

    with open(path, 'r') as f:
        for line in f.readlines():
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON on line: {line}. Error: {e}")
                continue  # Skip to the next line
            
            # Skip entries that don't meet the validation criteria
            if not is_valid(entry):
                continue
            
            # Exclude addresses that likely belong to apartments
            if entry['properties'].get('unit'):
                continue
            
            # Construct the address and coordinates for uniqueness verification
            address = (
                entry['properties']['number'],
                entry['properties']['street'],
                entry['properties']['city'],
                entry['properties']['region'],
                entry['properties']['postcode']
            )
            coords = tuple(entry['geometry']['coordinates'])
            
            unique_key = (address, coords)

            # Save the entry if it's unique
            if unique_key not in unique_entries:
                unique_entries.add(unique_key)
                cleaned_data.append(line)

    # Write the cleaned data to the output directory
    os.chdir(output_path)
    output_file = state + ".geojson"
    with open(output_file, 'w') as f:
        for line in cleaned_data:
            f.write(line)
   

def read_geojson_features(file_path):
    """
    Reads a geojson file and extracts its features.
    
    Args:
        file_path (str): Path to the .geojson file.

    Returns:
        list[dict]: A list of extracted features from the .geojson file.
    """
    
    features = []
    
    with open(file_path, 'r') as file:
        for line in file:
            try:
                feature = json.loads(line.strip())
                features.append(feature)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON on line: {line}. Error: {e}")
    
    return features

