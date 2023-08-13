import os

def delete_unwanted_files(path):
    """
    Delete all files in the directory and its subdirectories 
    except those named "statewide-addresses-state.geojson".
    
    :param path: Path to the directory.
    """
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename != "statewide-addresses-state.geojson":
                file_to_delete = os.path.join(dirpath, filename)
                try:
                    os.remove(file_to_delete)
                    print(f"Deleted: {file_to_delete}")
                except Exception as e:
                    print(f"Error deleting {file_to_delete}. Error: {e}")

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder: ")
    
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        delete_unwanted_files(folder_path)
        print("Finished deleting unwanted files.")
    else:
        print(f"'{folder_path}' is not a valid directory path.")
