import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from app.viewDataWin import ViewDataWin
from database.scripts.db import Data



@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

@pytest.fixture
def view_window(qapp):
    # Сбрасываем Singleton, чтобы база была свежая
    Data._instance = None
    window = ViewDataWin()
    yield window
    window.close()

# 1. Проверка, что таблица создаётся и имеет заголовки
def test_table_headers(view_window):
    assert view_window.table.columnCount() == 7
    headers = [view_window.table.horizontalHeaderItem(i).text() for i in range(view_window.table.columnCount())]
    assert headers == ['ID заказа', 'Тип работы', 'Описание', 'Дата принятия', 'Клиент', 'Исполнитель', 'Статус']

# 2. Проверка отображения данных после добавления записи
def test_table_after_add(view_window):
    order = {"type_of_work": "Repair", "description": "Fix PC", "acceptance_date": "2025-12-10",
             "customer": "Ivan", "executor": "Petrov", "status": "New"}
    view_window.db.add_order(**order)
    view_window.load_data()
    assert view_window.table.rowCount() >= 1

    # Проверяем, что хотя бы одна строка содержит "Repair"
    found = False
    for row in range(view_window.table.rowCount()):
        if view_window.table.item(row, 1).text() == "Repair":
            found = True
            break
    assert found



# 3. Проверка отображения данных после удаления записи
def test_table_after_delete(view_window):
    order = {"type_of_work": "Install", "description": "Setup OS", "acceptance_date": "2025-12-11",
             "customer": "Anna", "executor": "Sidorov", "status": "In Progress"}
    view_window.db.add_order(**order)
    view_window.load_data()
    initial_rows = view_window.table.rowCount()
    # Удаляем первую запись напрямую через db
    id_order = view_window.db.cur.execute("SELECT id_order FROM Orders").fetchone()[0]
    view_window.db.delete_order(id_order=id_order)
    view_window.load_data()
    assert view_window.table.rowCount() <= initial_rows - 1
