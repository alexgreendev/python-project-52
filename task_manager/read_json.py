import json
import os


def load_data(path):
    fixtures_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    data_path = os.path.join(fixtures_path, path)
    with open(data_path) as file:
        return json.loads(file.read())
