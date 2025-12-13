from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel)
from PyQt6.QtCore import Qt
from app.viewDataWin import ViewDataWindow
from app.addDataWin import AddDataWindow
from app.db import Database


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SRM-Система для работы со студентами")
        self.setGeometry(200, 200, 600, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.title_label = QLabel("Выберите что хотите сделать")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        self.view_button = QPushButton("Посмотреть базу студентов")
        self.add_button = QPushButton("Добавить студента в базу")
        self.exit_button = QPushButton("Выйти")


        layout.addWidget(self.view_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.exit_button)

        central_widget.setLayout(layout)

        self.view_button.clicked.connect(self.open_view_window)
        self.add_button.clicked.connect(self.open_add_window)
        self.exit_button.clicked.connect(self.close)

    def open_view_window(self):
        self.view_window = ViewDataWindow(self.db)
        self.view_window.show()

    def open_add_window(self):
        self.add_window = AddDataWindow(self.db)
        self.add_window.show()