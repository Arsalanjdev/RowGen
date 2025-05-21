import json
import os

from huggingface_hub import InferenceClient
import sqlalchemy
from dotenv import load_dotenv
from utils import API_KEY

print()


class JsonDB:
    def __init__(self):
        with open("db.json", "r") as f:
            self._json_raw = json.load(f)

    def get_column_names(self):
        return self._json_raw["columns"]

    def __getitem__(self, item):
        return self._json_raw[item]


print(JsonDB()["columns"])

client = InferenceClient(provider="novita", api_key=API_KEY)
completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3",
    messages=[
        {
            "role": "user",
            "content": f"generate 10 rows for the following schema: {JsonDB().get_column_names()}. Use real looking data (no john doe or @example.com. also make emails beliavble such as using numbers underscores. sometimes even use unrelated to emails that are unrelate to names.). do not say anything. just generate data in a json format.",
        }
    ],
)

print(completion.choices[0])


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


JsonParse(completion.choices[0].message["content"]).save_to_json()
