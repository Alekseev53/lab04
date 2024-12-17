from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from state_machine import TextProcessorStates
from process_functions import process_editor, process_generator, process_summarizer
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from process_functions import switch_model

# Главный экран "Экран выбора" с кнопками
async def show_main_menu(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Редактирование текста", "Генерация текста", "Суммаризация", "Изменить модель"]
    keyboard.add(*buttons)
    await TextProcessorStates.CHOOSING_MODE.set()  # Установить главное состояние
    await message.answer("Что дальше?", reply_markup=keyboard)

# Обработчик команды /start
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет! Я бот, помогающий работать с текстом.")
    await show_main_menu(message)

# Обработчики выбора кнопок

async def handle_editing(message: types.Message, state: FSMContext):
    # Переход на экран выбора стиля редактора
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Научный", "Литературный", "Зумерский")
    await TextProcessorStates.CHOOSING_EDITOR_STYLE.set()
    await message.answer("Выбор стиля редактирования:", reply_markup=keyboard)

async def handle_generation(message: types.Message, state: FSMContext):
    # Переход на экран выбора стиля генерации текста
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Научный", "Литературный", "Зумерский")
    await TextProcessorStates.CHOOSING_GENERATOR_STYLE.set()
    await message.answer("Выбор стиля генерации:", reply_markup=keyboard)

async def handle_summarization(message: types.Message, state: FSMContext):
    # Переход на экран выбора стиля суммаризации
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Подробный", "Краткий")
    await TextProcessorStates.CHOOSING_SUMMARIZER_STYLE.set()
    await message.answer("Выберите тип пересказа:", reply_markup=keyboard)

async def handle_model_change(message: types.Message, state: FSMContext):
    # Заглушка экрана изменения модели
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("GPT", "LLaMA")  # Варианты моделей
    await TextProcessorStates.CHOOSE_MODEL.set()
    await message.answer("Выберите модель:", reply_markup=keyboard)

# Обработчики выбора стиля
async def editor_style_chosen(message: types.Message, state: FSMContext):
    editor_style = message.text
    await state.update_data(editor_style=editor_style)
    await TextProcessorStates.EDIT_TEXT.set()  # Переход к следующему состоянию
    await message.answer("Теперь напишите текст, который нужно отредактировать.")

async def generation_style_chosen(message: types.Message, state: FSMContext):
    generation_style = message.text
    await state.update_data(generation_style=generation_style)
    await TextProcessorStates.GENERATE_TEXT.set()  # Переход к следующему состоянию
    await message.answer("Теперь напишите тему, для которой нужно сгенерировать текст.")

async def summarization_style_chosen(message: types.Message, state: FSMContext):
    summarization_style = message.text
    await state.update_data(summarization_style=summarization_style)
    await TextProcessorStates.SUMMARIZE_TEXT.set()  # Переход к следующему состоянию
    await message.answer("Введите текст для суммаризации.")

# Обработчики текста

async def edit_text_input(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    editor_style = user_data.get("editor_style")
    text_input = message.text
    await message.answer("Редактор приступил к работе, это может занять пару минут...")
    try:
        result = await process_editor(text_input, editor_style)
        await message.answer(f"Результат редактирования текста:\n\n{result}")
    except Exception as e:  # Обработка ошибок
        await message.answer(f"Произошла ошибка: {e}")
    await show_main_menu(message)  # Вернуться в главное меню

async def generate_text_input(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    generation_style = user_data.get("generation_style")
    text_input = message.text
    await message.answer("Писатель приступил к работе, это может занять пару минут...")
    try:
        result = await process_generator(text_input, generation_style)
        await message.answer(f"Сгенерированный текст:\n\n{result}")
    except Exception as e:  # Обработка ошибок
        await message.answer(f"Произошла ошибка: {e}")
    await show_main_menu(message)

async def summarize_text_input(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    summarization_style = user_data.get("summarization_style")
    text_input = message.text
    await message.answer("Суммаризатор приступил к работе, это может занять пару минут...")
    try:
        result = await process_summarizer(text_input, summarization_style)
        await message.answer(f"Суммаризация текста:\n\n{result}")
    except Exception as e:  # Обработка ошибок
        await message.answer(f"Произошла ошибка: {e}")
    await show_main_menu(message)

async def handle_model_change(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("GPT", "LLaMA")
    await TextProcessorStates.CHOOSE_MODEL.set()  # Установить состояние выбора модели
    await message.answer("Выберите модель:", reply_markup=keyboard)

async def model_chosen(message: types.Message, state: FSMContext):
    model_choice = message.text
    if model_choice not in ["GPT", "LLaMA"]:
        await message.answer("Пожалуйста, выберите модель из предложенных вариантов: GPT или LLaMA.")
        return

    switch_model(model_choice)  # Смена модели через функцию из process_functions.py
    await message.answer(f"Вы выбрали модель: {model_choice}.")
    await show_main_menu(message)

# Регистрация всех обработчиков
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(handle_editing, lambda msg: msg.text == "Редактирование текста", state=TextProcessorStates.CHOOSING_MODE)
    dp.register_message_handler(handle_generation, lambda msg: msg.text == "Генерация текста", state=TextProcessorStates.CHOOSING_MODE)
    dp.register_message_handler(handle_summarization, lambda msg: msg.text == "Суммаризация", state=TextProcessorStates.CHOOSING_MODE)
    dp.register_message_handler(handle_model_change, lambda msg: msg.text == "Изменить модель", state=TextProcessorStates.CHOOSING_MODE)

    dp.register_message_handler(editor_style_chosen, state=TextProcessorStates.CHOOSING_EDITOR_STYLE)
    dp.register_message_handler(generation_style_chosen, state=TextProcessorStates.CHOOSING_GENERATOR_STYLE)
    dp.register_message_handler(summarization_style_chosen, state=TextProcessorStates.CHOOSING_SUMMARIZER_STYLE)

    dp.register_message_handler(edit_text_input, state=TextProcessorStates.EDIT_TEXT)
    dp.register_message_handler(generate_text_input, state=TextProcessorStates.GENERATE_TEXT)
    dp.register_message_handler(summarize_text_input, state=TextProcessorStates.SUMMARIZE_TEXT)

    dp.register_message_handler(handle_model_change, lambda msg: msg.text == "Изменить модель", state=TextProcessorStates.CHOOSING_MODE)
    dp.register_message_handler(model_chosen, state=TextProcessorStates.CHOOSE_MODEL)  # Обработчик выбора из состояния CHOOSE_MODEL

async def handle_model_change(message: types.Message, state: FSMContext):
    """
    Обработчик изменения модели. Отображает варианты выбора.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("GPT", "LLaMA")
    await TextProcessorStates.CHOOSE_MODEL.set()  # Установить состояние выбора модели
    await message.answer("Выберите модель (GPT или LLaMA):", reply_markup=keyboard)

async def model_chosen(message: types.Message, state: FSMContext):
    """
    Обработчик выбора модели, переключения и возврата к главному меню.
    """
    model_choice = message.text.strip()
    if model_choice not in ["GPT", "LLaMA"]:
        await message.answer("Пожалуйста, выберите модель из предложенных вариантов: GPT или LLaMA.")
        return

    try:
        # Смена модели через ModelHandler
        switch_model(model_choice)
        await state.update_data(current_model=model_choice)  # Обновить контекст FSM
        await message.answer(f"Модель успешно изменена на: {model_choice}.")
    except Exception as e:
        await message.answer(f"Произошла ошибка при смене модели: {str(e)}")
        return

    # Возвращаем пользователя на главный экран
    await show_main_menu(message)