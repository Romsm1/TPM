import pytest
import sys, os
import tempfile
from PyQt6.QtWidgets import QApplication

# Добавляем путь к проекту, чтобы импорты работали
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.scripts.db import Data
import database.scripts.db as db_module
from app.addDataWin import AddDataWin
from app.mainWin import MainWin
from app.viewDataWin import ViewDataWin

# QApplication фикстура
# создаётся один раз на всю сессию тестов
@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app

# Временная база данных
# создаётся для каждого теста и удаляется после
@pytest.fixture
def temp_db():
    # сбрасываем Singleton, чтобы база была свежая
    db_module.Data._instance = None

    # создаём временный файл SQLite
    db_file = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
    db_path = db_file.name
    db_file.close()

    # создаём объект базы данных
    db = db_module.Data(db_path)

    # создаём все нужные таблицы
    db.cur.execute("""
        CREATE TABLE Orders (
            id_order INTEGER PRIMARY KEY AUTOINCREMENT,
            type_of_work TEXT,
            description TEXT,
            acceptance_date TEXT,
            customer TEXT,
            executor TEXT,
            status TEXT
        );
    """)
    db.cur.execute("CREATE TABLE WorkTypes (id_work INTEGER PRIMARY KEY AUTOINCREMENT, work TEXT);")
    db.cur.execute("CREATE TABLE Executors (id_employee INTEGER PRIMARY KEY AUTOINCREMENT, employee TEXT);")
    db.cur.execute("CREATE TABLE Statuses (id_status INTEGER PRIMARY KEY AUTOINCREMENT, status TEXT);")
    db.db.commit()

    # добавляем тестовые значения для ComboBox
    db.cur.execute("INSERT INTO WorkTypes (work) VALUES ('Repair')")
    db.cur.execute("INSERT INTO Executors (employee) VALUES ('Petrov')")
    db.cur.execute("INSERT INTO Statuses (status) VALUES ('New')")
    db.db.commit()

    # возвращаем объект базы в тест
    yield db

    # закрываем и удаляем временный файл после теста
    db.db.close()
    os.remove(db_path)

# Фикстура для окна добавления заказа
@pytest.fixture
def add_window(qapp, temp_db):
    window = AddDataWin(temp_db)
    yield window
    window.close()

# Фикстура для окна просмотра заказов
@pytest.fixture
def view_window(qapp, temp_db):
    window = ViewDataWin(temp_db)
    yield window
    window.close()

# Фикстура для главного окна приложения
@pytest.fixture
def main_window(qapp, temp_db):
    window = MainWin()
    window.db = temp_db
    yield window
    window.close()
