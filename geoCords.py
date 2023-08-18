import json

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


