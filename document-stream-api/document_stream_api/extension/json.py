import json
import sqlite3


class JSONEncoder(json.JSONEncoder):
    def default(self, data):
        if isinstance(data, sqlite3.Row):
            return {key: data[key] for key in data.keys()}
        return data
