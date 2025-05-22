import json
from rowgen.json_parser import JsonParse
from rowgen.hf_api import HFapi
from pytest import fixture


@fixture
def hfapi():
    return HFapi()


def test_rows_json(hfapi):
    raw_query = hfapi.send_message_to_api(
        "This is my database: id, name, username, email, access_level. generate 5 fake data rows for it. don't say anything just generate in json. i want your whole message to be just a json"
    )
    jsp = JsonParse(raw_query)
    try:
        json.loads(jsp.processed_query)
        return True
    except json.JSONDecodeError:
        return False
