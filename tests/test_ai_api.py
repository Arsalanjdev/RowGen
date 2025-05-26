from os import getenv
from pathlib import Path

import pytest
from dotenv import load_dotenv
from huggingface_hub import HfApi, InferenceClient
from huggingface_hub.errors import BadRequestError

from rowgen.hf_api import HFapi

DEEP_SEEK_MODEL = "deepseek-ai/DeepSeek-V3"

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
API_KEY = getenv("HF_API_KEY")


@pytest.fixture
def inference_client():
    client = InferenceClient(provider="novita", api_key=API_KEY)
    yield client
    # Teardown (if needed) goes here


@pytest.fixture
def hf_api_client():
    return HfApi(API_KEY)


@pytest.fixture
def hf_api():
    client = HFapi(API_KEY)
    return client


# def test_hf_hub_ping(hf_api_client):
#     try:
#         info = hf_api_client.model_info(DEEP_SEEK_MODEL)
#         assert info.modelId == DEEP_SEEK_MODEL
#         print("Ping successful: Connected to Hugging Face Hub.")
#     except Exception as e:
#         pytest.fail(f"Failed to ping Hugging Face Hub: {e}")
#


def test_hf_api_send_message_to_api(hf_api):
    prompt_message = "Hi! This is a test. say banana if you can hear me."
    try:
        response_message = hf_api.send_message_to_api(prompt_message)
        assert len(response_message) > 0
        assert "banana" in response_message.casefold()

    except BadRequestError as e:
        print(e)

    except Exception as d:
        pytest.fail(f"Failed inference call: {d}")


def test_hf_sql_message(hf_api):
    prompt_message = "Write five sql statements for the table Books made up of id, title, isbn, genre, publication_date, author. Your message should only consist of sql statements with no sentence before and after."
    try:
        response_message = hf_api.send_message_to_api(prompt_message)
        assert len(response_message) > 0
        assert response_message.startswith("```sql")
        assert response_message.endswith("```")

    except BadRequestError as e:
        print(e)

    except Exception as d:
        pytest.fail(f"Failed inference call: {d}")
