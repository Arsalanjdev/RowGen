import os

import pytest
from dotenv import load_dotenv
from huggingface_hub.errors import BadRequestError

from rowgen.utils import API_KEY
from huggingface_hub import InferenceClient, HfApi


DEEP_SEEK_MODEL = "deepseek-ai/DeepSeek-V3"


@pytest.fixture
def inference_client():
    client = InferenceClient(provider="novita", api_key=API_KEY)
    yield client
    # Teardown (if needed) goes here


@pytest.fixture
def hf_api_client():
    return HfApi()


def test_hf_hub_ping(hf_api_client):
    try:
        info = hf_api_client.model_info(DEEP_SEEK_MODEL)
        assert info.modelId == DEEP_SEEK_MODEL
        print("Ping successful: Connected to Hugging Face Hub.")
    except Exception as e:
        pytest.fail(f"Failed to ping Hugging Face Hub: {e}")


def test_hf_inference_connection(inference_client):
    prompt_message = "Hi! This is a test. say banana if you can hear me."
    try:
        completion = inference_client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[{"role": "user", "content": prompt_message}],
        )
        message: str = completion.choices[0].message["content"]
        assert len(message) > 0
        assert "banana" in message.casefold()

    except BadRequestError as e:
        print(e)

    except Exception as d:
        pytest.fail(f"Failed inference call: {d}")
