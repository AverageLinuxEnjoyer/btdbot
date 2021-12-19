import json

def load_strategy(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)
        return data