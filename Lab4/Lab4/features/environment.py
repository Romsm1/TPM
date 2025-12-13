import sys
import os
import tempfile
import time
from PyQt6.QtWidgets import QApplication

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db import Database


class TestContext:
    def __init__(self):  # Класс для хранения контекста тестирования
        self.app = None  # GUI-приложение Qt
        self.main_window = None
        self.current_window = None
        self.temp_db_path = None  # Путь к временной БД для тестов
        self.db = None  # Объект подключения к БД
        self.test_data = []

def before_all(context):  # Выполняется перед всеми тестами
    context.test_context = TestContext()  # Инициализация контекста тестирования
    context.test_context.temp_db_path = tempfile.NamedTemporaryFile(
        suffix='.db', delete=False  # Создание временного файла БД
    ).name
    if QApplication.instance() is None:  # Проверка существования QApplication
        context.test_context.app = QApplication([])
    else:
        context.test_context.app = QApplication.instance()  # Использование существующего

def before_scenario(context, scenario):  # Выполняется перед каждым сценарием
    if os.path.exists(context.test_context.temp_db_path):  # Очистка старой БД если существует
        if hasattr(context.test_context, 'db') and context.test_context.db:
            if hasattr(context.test_context.db, 'close'):
                context.test_context.db.close()  # Закрытие соединения с БД
        time.sleep(0.1)
        for _ in range(3):  # Попытки удаления файла БД
            try:
                os.remove(context.test_context.temp_db_path)  # Удаление файла
                break
            except PermissionError:
                time.sleep(0.1)
    context.test_context.db = Database(context.test_context.temp_db_path)  # Создание новой БД
    context.db = context.test_context.db  # Сохраняем ссылку на БД в контексте Behave

def after_scenario(context, scenario):  # Выполняется после каждого сценария
    if hasattr(context, 'windows'):  # Закрытие всех окон тестирования
        for window in context.windows:
            if hasattr(window, 'close'):
                window.close()
    if hasattr(context, 'temp_files'):  # Удаление временных файлов
        for temp_file in context.temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass

def after_all(context):  # Выполняется после всех тестов
    if context.test_context.app:
        context.test_context.app.quit()  # Завершение GUI-приложения
    if (context.test_context.temp_db_path and
        os.path.exists(context.test_context.temp_db_path)):  # Удаление временной БД
        try:
            os.remove(context.test_context.temp_db_path)
        except:
            pass
