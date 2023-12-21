# Импортируем необходимые модули
import subprocess
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QRadioButton, QTimeEdit, QListWidget,
                             QVBoxLayout, QHBoxLayout)
from PyQt6.QtCore import QTimer, QTime


class TimeTracker(QWidget):
    def __init__(self):
        super().__init__()
        # заголовок, размер и положение окна
        self.setWindowTitle('Time Tracker')
        self.resize(400, 500)
        # виджеты для кнопок, переключателей, таймера и списка
        self.start_button = QPushButton('Старт')
        self.pause_button = QPushButton('Пауза')
        self.stop_button = QPushButton('Стоп')
        self.report_button = QPushButton('Отчет')
        self.all_time_radio = QRadioButton('All time')
        self.timer_radio = QRadioButton('Timer')
        self.time_edit = QTimeEdit()
        self.process_list = QListWidget()
        # кнопка паузы и таймер по умолчанию
        self.pause_button.setEnabled(False)
        self.time_edit.setEnabled(False)
        # таймер для отслеживания времени
        self.timer = QTimer()
        # словарь для хранения процессов и времени
        self.processes = {}
        # переменная для хранения текущего процесса
        self.current_process = None
        # переменная для хранения времени начала процесса
        self.start_time = None
        # переменная для хранения времени паузы
        self.pause_time = None
        # переменная для хранения режима работы
        self.mode = 'All time'
        # переменная для хранения лимита времени
        self.limit = None
        # переменная для хранения общего времени
        self.total_time = 0
        # сигналы и слоты для обработки событий

        # макеты для размещения виджетов
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.main_layout = QHBoxLayout()
        # виджеты в макетах
        self.left_layout.addWidget(self.start_button)
        self.left_layout.addWidget(self.pause_button)
        self.left_layout.addWidget(self.stop_button)
        self.left_layout.addWidget(self.report_button)
        self.left_layout.addWidget(self.all_time_radio)
        self.left_layout.addWidget(self.timer_radio)
        self.left_layout.addWidget(self.time_edit)
        self.right_layout.addWidget(self.process_list)
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
        # главный макет для окна
        self.setLayout(self.main_layout)
        # Показываем окно
        self.show()


app = QApplication(sys.argv)
window = TimeTracker()
window.show()
sys.exit(app.exec())
