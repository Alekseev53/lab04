from models.gpt_model import GPTModel
from models.llama_model import LLAMAModel

class ModelHandler:
    def __init__(self, model_type: str = "GPT"):
        """
        Инициализация ModelHandler с выбранным типом модели.
        :param model_type: Может быть "GPT" или "LLaMA".
        """
        self.model_type = model_type
        self.model = self._initialize_model()

    def _initialize_model(self):
        """
        В зависимости от значения self.model_type возвращает экземпляр модели.
        """
        if self.model_type == "GPT":
            return GPTModel()
        elif self.model_type == "LLaMA":
            return LLAMAModel()
        else:
            raise ValueError(f"Неизвестный тип модели: {self.model_type}")

    def switch_model(self, model_type: str):
        """
        Меняет текущую модель на указанную.
        """
        self.model_type = model_type
        self.model = self._initialize_model()
        print(f"Текущая модель изменена на: {self.model_type}")  # Вывод текущей модели

    async def generate_response(self, prompt: str) -> str:
        """
        Генерирует ответ, используя текущую модель.
        """
        return await self.model.generate_response(prompt)