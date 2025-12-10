import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QApplication
from app.addDataWin import AddDataWin
from database.scripts.db import Data


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

@pytest.fixture
def add_window(qapp):
    # Сбрасываем Singleton, чтобы база была свежая
    Data._instance = None
    window = AddDataWin()
    yield window
    window.close()

# 1. Проверка правильности добавления данных
def test_add_order(add_window):
    add_window.work_input.setCurrentIndex(0)
    add_window.description_input.setText("Test description")
    add_window.date_input.setText("2025-12-10")
    add_window.customer_input.setText("Ivan")
    add_window.executor_input.setCurrentIndex(0)
    add_window.status_input.setCurrentIndex(0)

    add_window.add_order()
    rows = add_window.db.cur.execute("SELECT * FROM Orders").fetchall()
    assert any("Test description" in row for row in [r[2] for r in rows])

# 2. Проверка корректного сохранения отредактированных данных
def test_edit_order(add_window):
    # Сначала добавляем запись
    add_window.work_input.setCurrentIndex(0)
    add_window.description_input.setText("Old description")
    add_window.date_input.setText("2025-12-11")
    add_window.customer_input.setText("Anna")
    add_window.executor_input.setCurrentIndex(0)
    add_window.status_input.setCurrentIndex(0)
    add_window.add_order()

    # Берём id добавленной записи
    id_order = add_window.db.cur.execute("SELECT id_order FROM Orders").fetchone()[0]
    data = [id_order, "Repair", "Old description", "2025-12-11", "Anna", "Petrov", "New"]

    # Открываем окно редактирования
    edit_win = AddDataWin(data)
    edit_win.description_input.setText("Updated description")
    edit_win.add_order()

    row = edit_win.db.cur.execute("SELECT description FROM Orders WHERE id_order=?", (id_order,)).fetchone()
    assert row[0] == "Updated description"

# 3. Проверка реакции на невалидные данные
def test_invalid_order(add_window):
    add_window.work_input.setCurrentIndex(0)
    add_window.description_input.setText("")
    add_window.date_input.setText("")
    add_window.customer_input.setText("")
    add_window.executor_input.setCurrentIndex(0)
    add_window.status_input.setCurrentIndex(0)

    add_window.add_order()
    rows = add_window.db.cur.execute("SELECT * FROM Orders").fetchall()
    # проверяем, что запись с пустым description действительно есть
    assert any(r[2] == "" for r in rows)
