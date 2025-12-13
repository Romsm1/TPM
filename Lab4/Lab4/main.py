import sys
import traceback
from PyQt6.QtWidgets import QApplication
from app.mainWin import MainWindow


def custom_excepthook(exc_type, exc_value, exc_tb):
    print("Ошибка:", "".join(traceback.format_exception(exc_type, exc_value, exc_tb)))


def start_app():
    sys.excepthook = custom_excepthook
    qt_app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    sys.exit(qt_app.exec())


if __name__ == '__main__':
    start_app()


""" pip install -r requirements.txt """
""" python -m behave features/ """