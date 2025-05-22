import json
from rowgen.parser import parse_sql_from_code_block
from rowgen.hf_api import HFapi
from pytest import fixture


@fixture
def hfapi():
    return HFapi()
