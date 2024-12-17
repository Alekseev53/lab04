from models.model_class import ModelHandler

# Инициализация обработчика модели с начальной моделью (по умолчанию GPT)
model_handler = ModelHandler(model_type="GPT")

async def process_editor(text: str, editor_style: str) -> str:
    """
    Обработка текста в выбранном стиле с использованием активной модели.
    """
    prompt = f"Напиши текст в {editor_style} стиле: {text}"
    response = await model_handler.generate_response(prompt)
    return response

async def process_generator(topic: str, generation_style: str) -> str:
    """
    Генерация текста по теме с использованием активной модели.
    """
    prompt = f"Сгенерируй текст на тему '{topic}' в {generation_style} стиле."
    response = await model_handler.generate_response(prompt)
    return response

async def process_summarizer(text: str, summary_style: str) -> str:
    """
    Суммаризация текста в указанном стиле с использованием активной модели.
    """
    prompt = f"Создай {summary_style} пересказ для текста: {text}"
    response = await model_handler.generate_response(prompt)
    return response

def switch_model(model_type: str):
    """
    Меняет текущую модель, обновляя ModelHandler.
    """
    try:
        model_handler.switch_model(model_type)  # Сменить модель в существующем ModelHandler
        print(f"Текущая модель успешно изменена на: {model_type}")  # Вывод в лог
    except ValueError as e:
        print(f"Ошибка при переключении модели: {e}")  # Возможный лог или сообщение для отладки
        raise RuntimeError(f"Не могу переключить модель: {e}")