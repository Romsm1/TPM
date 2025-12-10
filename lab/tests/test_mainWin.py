import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from app.mainWin import MainWin
from app.viewDataWin import ViewDataWin
from app.addDataWin import AddDataWin



# QApplication фикстура
@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

@pytest.fixture
def main_window(qapp):
    window = MainWin()
    yield window
    window.close()

# 1. Проверка наличия кнопок
def test_widgets_exist(main_window):
    assert hasattr(main_window, "view_data_btn")
    assert hasattr(main_window, "add_data_btn")
    assert main_window.view_data_btn.text() == "Просмотреть"
    assert main_window.add_data_btn.text() == "Добавить"

# 2. Проверка заголовка окна
def test_window_title(main_window):
    assert main_window.windowTitle() == "Сервисный центр"

# 3. Проверка закрытия окна (удаление)
def test_window_close(main_window, qtbot):
    qtbot.addWidget(main_window)
    main_window.close()
    assert not main_window.isVisible()

# 4. Проверка открытия окна просмотра
def test_view_button_opens_window(main_window, qtbot):
    qtbot.mouseClick(main_window.view_data_btn, Qt.MouseButton.LeftButton)
    assert isinstance(main_window.win_v, ViewDataWin)
    assert main_window.win_v.isVisible()

# 5. Проверка открытия окна добавления
def test_add_button_opens_window(main_window, qtbot):
    qtbot.mouseClick(main_window.add_data_btn, Qt.MouseButton.LeftButton)
    assert isinstance(main_window.win_a, AddDataWin)
    assert main_window.win_a.isVisible()