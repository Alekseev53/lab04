import requests
import aiohttp
import os

class LLAMAModel:
    def __init__(self):
        """
        Класс для асинхронного взаимодействия с моделью через API.
        """
        self.base_url = f"http://{os.getenv('SERVER_IP')}/generate"

    async def generate_response(self, prompt: str) -> str:
        """
        Асинхронно отправляет запрос на генерацию текста к модели.
        
        :param prompt: Стартовый текст или сообщение для модели.
        :param model: Тип модели для генерации (например, "llama").
        :return: Сгенерированный текст от модели.
        """
        payload = {'prompt': prompt, 'model': "llama"}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.base_url, json=payload) as response:
                    response_data = await response.json()
                    return response_data.get("text", "Ошибка: не удалось получить сгенерированный текст.")
            except aiohttp.ClientError as e:
                return f"Ошибка при обращении к API: {e}"
            except Exception as e:
                return f"Произошла непредвиденная ошибка: {e}"
