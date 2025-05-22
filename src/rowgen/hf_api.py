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

    def prompt_fake_data(self, db_schema: str, num_rows: int = 10) -> str:
        """
        Generates a prompt based on the DB information it recieves
        :return: str. the response of ai api.
        """
        prompt = f"""
        Generate {num_rows} rows of fake sql data for the following table:column schema. Make the data look believable and realistic (not john doe or anything like that). 
        Your response should be only in plain json with no words before or after. table:column schema: {db_schema}
        """
        return self.send_message_to_api(prompt)

    def prompt_insert_statements(self, jsondata: str, table_name: str):
        prompt = f"""Given the following jsondata that is to be inserted into a SQL table (table_name:{table_name}, generate insert statements for it. Your output should only be insert statements without any sentences before or after. data: {jsondata}"""
        return self.send_message_to_api(prompt)
