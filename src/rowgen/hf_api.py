from huggingface_hub import InferenceClient

from rowgen.utils import API_KEY


class HFapi:
    def __init__(self, provider: str = "novita", api_key: str = API_KEY):
        self.client = InferenceClient(provider=provider, api_key=api_key)

    def send_message_to_api(self, message: str) -> str:
        """
        Sends a message to the AI and returns the response
        :param message: The prompt to be sent.
        :return: the response of AI model.
        """
        completion = self.client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
        )
        return completion.choices[0].message["content"]
