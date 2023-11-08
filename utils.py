import json
import os


def load_schema(name):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'json_schemas', name)
    with open(path) as file:
        json_schema = json.loads(file.read())
    return json_schema
