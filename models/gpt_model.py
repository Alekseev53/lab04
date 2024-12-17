import json
import os
import aiohttp

class GPTModel:
    def __init__(self):
        """
        Класс для асинхронного взаимодействия с моделью Yandex GPT через API.
        """
        self.name = "Yandex GPT Model"
        self.headers = self._get_auth_headers()
        self.url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'

    def _get_auth_headers(self):
        if os.getenv('IAM_TOKEN') is not None:
            iam_token = os.environ['IAM_TOKEN']
            return {'Authorization': f'Bearer {iam_token}'}
        elif os.getenv('API_KEY') is not None:
            api_key = os.environ['API_KEY']
            return {'Authorization': f'Api-Key {api_key}'}
        else:
            raise ValueError("Не установлен IAM_TOKEN или API_KEY в переменных окружения")

    async def generate_response(self, prompt: str) -> str:
        body = {
            "modelUri": f"gpt://{os.getenv('YANDEX_FOLDER_ID')}/{os.getenv('YANDEX_MODEL_NAME')}",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 2000
            },
            "messages": [
                {"role": "system", "text": "Ты умный ассистент"},
                {"role": "user", "text": prompt}
            ]
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.url, headers=self.headers, json=body) as response:

                    # Проверка статуса ответа
                    if response.status != 200:
                        raise RuntimeError(
                            f"Invalid response received: code: {response.status}, message: {await response.text()}"
                        )

                    # Парсинг ответа
                    data = await response.json()
                    result_text = data["result"]["alternatives"][0]["message"]["text"]
                    return result_text.strip()

            except Exception as e:
                return f"Ошибка при запросе к Яндекс GPT: {str(e)}"