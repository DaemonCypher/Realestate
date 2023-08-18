import os

def delete_unwanted_files(path):
    """
    Delete all files in the directory and its subdirectories 
    except those named "statewide-addresses-state.geojson".
    
    :param path: Path to the directory.
    """
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
