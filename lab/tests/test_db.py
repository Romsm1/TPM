import pytest
import tempfile
import os
import sys

# Добавляем lab в sys.path, чтобы импорты работали при запуске тестов
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import database.scripts.db as db_module
from database.scripts.db import Data


@pytest.fixture
def temp_db():
    # Сбрасываем Singleton, чтобы каждый тест создавал новое соединение
    db_module.Data._instance = None

    # создаём временный файл SQLite
    db_file = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
    db_path = db_file.name
    db_file.close()

    # создаём объект базы данных
    db = Data(db_path)

    # создаём таблицу Orders для тестов
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
    db.db.commit()

    # возвращаем объект базы в тест
    yield db

    # закрываем соединение и удаляем временный файл после теста
    db.db.close()
    os.remove(db_path)


# Параметризованный тест добавления заказов
@pytest.mark.parametrize("order", [
    {"type_of_work": "Repair", "description": "Fix PC", "acceptance_date": "2025-12-10",
     "customer": "Ivan", "executor": "Petrov", "status": "New"},
    {"type_of_work": "Install", "description": "Setup OS", "acceptance_date": "2025-12-11",
     "customer": "Anna", "executor": "Sidorov", "status": "In Progress"},
])
def test_add_order(temp_db, order):
    # добавляем заказ
    result = temp_db.add_order(**order)
    assert result == "Запись добавлена"

    # проверяем, что запись появилась в таблице
    rows = temp_db.cur.execute("SELECT * FROM Orders").fetchall()
    assert len(rows) > 0


def test_update_order(temp_db):
    # добавляем заказ
    order = {"type_of_work": "Repair", "description": "Fix PC", "acceptance_date": "2025-12-10",
             "customer": "Ivan", "executor": "Petrov", "status": "New"}
    temp_db.add_order(**order)

    # получаем id добавленной записи
    id_order = temp_db.cur.execute("SELECT id_order FROM Orders").fetchone()[0]

    # обновляем статус заказа
    updated = {**order, "id_order": id_order, "status": "Done"}
    result = temp_db.update_order(**updated)
    assert result == "Запись обновлена"

    # проверяем, что статус изменился
    row = temp_db.cur.execute("SELECT status FROM Orders WHERE id_order=?", (id_order,)).fetchone()
    assert row[0] == "Done"


def test_delete_order(temp_db):
    # добавляем заказ
    order = {"type_of_work": "Repair", "description": "Fix PC", "acceptance_date": "2025-12-10",
             "customer": "Ivan", "executor": "Petrov", "status": "New"}
    temp_db.add_order(**order)

    # получаем id добавленной записи
    id_order = temp_db.cur.execute("SELECT id_order FROM Orders").fetchone()[0]

    # удаляем заказ
    result = temp_db.delete_order(id_order=id_order)
    assert result == "Запись удалена"

    # проверяем, что запись удалена
    row = temp_db.cur.execute("SELECT * FROM Orders WHERE id_order=?", (id_order,)).fetchone()
    assert row is None


# Метод получения всех заказов (пример реализации)
def get_all_orders(self, filter_field=None, filter_value=None):
    try:
        # если передан фильтр — выбираем по условию
        if filter_field and filter_value:
            self.cur.execute(f"SELECT * FROM Orders WHERE {filter_field}=?", (filter_value,))
        else:
            # иначе выбираем все записи
            self.cur.execute("SELECT * FROM Orders")
        return self.cur.fetchall()
    except sqlite3.OperationalError as e:
        # если таблицы нет — возвращаем пустой список
        return []
