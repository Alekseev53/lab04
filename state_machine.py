from aiogram.dispatcher.filters.state import State, StatesGroup

# Все состояния экрана
class TextProcessorStates(StatesGroup):
    CHOOSING_MODE = State()                  # Экран Выбор
    CHOOSING_EDITOR_STYLE = State()          # Экран Выбор стиля редактирования
    CHOOSING_GENERATOR_STYLE = State()       # Экран Выбор стиля генерации
    CHOOSING_SUMMARIZER_STYLE = State()      # Экран Выбор стира суммаризации
    EDIT_TEXT = State()                      # Экран Редактирование текста
    GENERATE_TEXT = State()                  # Экран Генератор текста
    SUMMARIZE_TEXT = State()                 # Экран Суммаризатор текста
    CHOOSE_MODEL = State()                   # Экран Изменить модель