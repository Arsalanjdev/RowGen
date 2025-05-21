import json
import os

from huggingface_hub import InferenceClient
import sqlalchemy
from dotenv import load_dotenv
from utils import API_KEY


class JsonDB:
    def __init__(self):
        with open("db.json", "r") as f:
            self._json_raw = json.load(f)

    def get_column_names(self):
        return self._json_raw["columns"]

    def __getitem__(self, item):
        return self._json_raw[item]


print(JsonDB()["columns"])


class JsonParse:
    def __init__(self, query: str):
        self._raw_query = query
        self.processed_query = JsonParse.trun_query(self._raw_query)

    @staticmethod
    def trun_query(query: str) -> str:
        if query.startswith("```json"):
            query = query.removeprefix("```json").strip()
        elif query.startswith("```"):
            query = query.removeprefix("```").strip()

        if query.endswith("```"):
            query = query.removesuffix("```").strip()

        return query

    def save_to_json(self, file_path: str = "output.json"):
        try:
            data = json.loads(self.processed_query)
        except json.JSONDecodeError as e:
            print("failed to parse json", e)
            print(self.processed_query)
            return

        with open(file_path, "w") as f:
            json.dump(data, f)
