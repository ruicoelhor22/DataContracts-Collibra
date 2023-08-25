import yaml

def read_yaml_file(file_path):
    with open (file_path, 'r') as file:
        data =yaml.safe_load(file)
    return data

if __name__ == "__main__" :
    file_path = "cenas.yml"
    try:
        yaml_data = read_yaml_file(file_path)
        print("Successfully read YAML file:")
        print(yaml_data)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse YAML file. {e}")