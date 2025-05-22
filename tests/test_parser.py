import json
from rowgen.parser import parse_sql_from_code_block, parse_json_from_code_block
from rowgen.hf_api import HFapi
from pytest import fixture


@fixture
def hfapi():
    return HFapi()


def test_rows_json(hfapi):
    raw_query = hfapi.send_message_to_api(
        "This is my database: id, name, username, email, access_level. generate 5 fake data rows for it. don't say anything just generate in json. i want your whole message to be just a json"
    )
    jsp = parse_json_from_code_block(raw_query)
    try:
        json.loads(jspy)
        return True
    except json.JSONDecodeError:
        return False
