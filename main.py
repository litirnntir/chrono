import datetime
import subprocess
import sys
import time

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QRadioButton, QTimeEdit,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QLabel, QTableWidget, QHeaderView,
                             QAbstractItemView, QTableWidgetItem)
from PyQt6.QtCore import QTimer, QTime


def message(text="", icon_path=None, title=""):
    msg = QMessageBox()
    if icon_path:
        pixmap = QPixmap(icon_path)
        msg.setIconPixmap(pixmap)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.exec()


def get_active_app_name():
    script = """
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
    end tell
    return frontApp
    """
    output = subprocess.check_output(["osascript", "-e", script])
    return output.strip().decode("utf-8")


class TimeTracker(QWidget):
    def __init__(self):
        super().__init__()
        # заголовок, размер и положение окна
        self.setWindowTitle('Хронометраж работы')
        self.setFixedSize(600, 600)
        # Общее время
        self.label_total_time = QLabel("Прошло времени: 00:00:00")
        self.label_total_time.setFixedSize(200, 20)
        # виджеты для кнопок, переключателей, таймера и списка
        self.start_button = QPushButton('Старт')
        self.pause_button = QPushButton('Пауза')
        self.stop_button = QPushButton('Стоп')
        self.report_button = QPushButton('Отчет')
        self.all_time_radio = QRadioButton('Без лимита')
        self.timer_radio = QRadioButton('С лимитом')
        self.time_edit = QTimeEdit()
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(2)
        self.process_table.setHorizontalHeaderLabels(["Приложение", "Время"])
        self.process_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.process_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)
        self.process_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection)
        self.process_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.pause_button.setEnabled(False)
        self.time_edit.setEnabled(False)
        self.timer = QTimer()
        self.processes = {}  # процессы и время
        self.current_process = None
        self.start_time = None
        self.pause_time = None
        self.mode = 'All time'
        self.limit = None
        self.total_time = 0
        # сигналы и слоты для обработки событий
        self.start_button.clicked.connect(self.start)
        self.pause_button.clicked.connect(self.pause)
        self.stop_button.clicked.connect(self.stop)
        self.report_button.clicked.connect(self.report)
        # сигналы и слоты для таймера и переключателя
        self.all_time_radio.toggled.connect(self.set_mode)
        self.all_time_radio.setChecked(True)
        self.timer_radio.toggled.connect(self.set_mode)
        self.time_edit.timeChanged.connect(self.set_limit)
        self.timer.timeout.connect(self.update)
        # макеты для размещения виджетов
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.main_layout = QHBoxLayout()
        # виджеты в макетах
        self.left_layout.addWidget(self.label_total_time)
        self.left_layout.addWidget(self.start_button)
        self.left_layout.addWidget(self.pause_button)
        self.left_layout.addWidget(self.stop_button)
        self.left_layout.addWidget(self.report_button)
        self.left_layout.addWidget(self.all_time_radio)
        self.left_layout.addWidget(self.timer_radio)
        self.left_layout.addWidget(self.time_edit)
        self.right_layout.addWidget(self.process_table)
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
        # главный макет для окна
        self.setLayout(self.main_layout)
        self.show()

        # Метод для обработки переключения режима работы

    def set_mode(self):
        radio = self.sender()
        if radio.isChecked():
            self.mode = radio.text()
            if self.mode == 'С лимитом':
                self.time_edit.setEnabled(True)
                self.set_limit(self.time_edit.time())
            else:
                self.time_edit.setEnabled(False)
                self.limit = None

    # Метод для установки лимита времени
    def set_limit(self, time):
        self.limit = time.hour() * 3600 + time.minute() * 60 + time.second()

    def report(self):
        # Обновить время для текущего процесса
        self.current_process = None

        with open("time_stats.txt", "w") as f:
            f.write(f"Общее время: {self.total_time}\n\n")
            f.write(f"Время в приложениях:\n")
            for app, time in self.processes.items():
                f.write(f"{{{app}: {str(datetime.timedelta(seconds=time))}}}\n")

        message('Статистика успешно загружена', icon_path=None, title="Успешно")

    def start(self):
        self.set_mode()
        self.timer_radio.setEnabled(False)
        self.all_time_radio.setEnabled(False)
        self.time_edit.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.timer.start(1000)
        message('Считывание процессов начато', icon_path=None, title="Успешно")

    def pause(self):
        self.pause_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.current_process = None
        self.timer.stop()
        self.pause_time = QTime.currentTime()

    # Метод для обработки нажатия на кнопку Стоп
    def stop(self):
        self.timer_radio.setEnabled(True)
        self.all_time_radio.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.timer.stop()
        self.current_process = None
        self.current_process = None
        self.start_time = None
        self.total_time = 0
        self.report()
        self.processes = {}
        self.process_table.clear()
        self.process_table.setRowCount(0)
        self.process_table.setColumnCount(0)

        # Выводим сообщение о завершении считывания процессов
        message('Считывание процессов завершено', icon_path=None, title="Успешно")

    def add_to_table(self):
        self.process_table.setRowCount(len(self.processes))
        row = 0
        for app, time in self.processes.items():
            app_item = QTableWidgetItem(app)
            time_item = QTableWidgetItem(str(datetime.timedelta(seconds=time)))
            self.process_table.setItem(row, 0, app_item)
            self.process_table.setItem(row, 1, time_item)
            row += 1

    def add_time_stats(self, app_name):
        if app_name != self.current_process:
            self.add_to_table()
        if app_name in self.processes:
            self.processes[app_name] += 1
        else:
            self.processes[app_name] = 1

    # Главный метод обработки
    def update(self):
        active_process = get_active_app_name()
        self.add_time_stats(active_process)
        self.current_process = get_active_app_name()
        if self.mode == 'С лимитом' and self.total_time >= self.limit:
            self.stop()
        else:
            self.total_time += 1
        self.label_total_time.setText("Прошло времени: " + (time.strftime("%H:%M:%S", time.gmtime(self.total_time))))


app = QApplication(sys.argv)
window = TimeTracker()
window.show()
sys.exit(app.exec())
