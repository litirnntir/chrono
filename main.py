import subprocess
import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QRadioButton, QTimeEdit, QListWidget,
                             QVBoxLayout, QHBoxLayout, QMessageBox)
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
        self.timer.timeout.connect(self.update)
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
        self.start_button.clicked.connect(self.start)
        self.pause_button.clicked.connect(self.pause)
        self.stop_button.clicked.connect(self.stop)
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

    def start(self):
        message('Считывание процессов начато', icon_path=None, title="Успешно")
        self.timer.start(1000)
        self.pause_button.setEnabled(True)
        self.start_button.setEnabled(False)

    def pause(self):
        # Деактивируем кнопку паузы и активируем кнопку старт
        self.pause_button.setEnabled(False)
        self.start_button.setEnabled(True)
        # TODO: Обновить время для текущего процесса
        # self.update_time()
        # Останавливаем таймер
        self.timer.stop()
        # Запоминаем время паузы
        self.pause_time = QTime.currentTime()

    # Метод для обработки нажатия на кнопку Стоп
    def stop(self):
        # Деактивируем кнопки паузы и стоп и активируем кнопку старт
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        # Останавливаем таймер
        self.timer.stop()
        #TODO: Обновить время для текущего процесса
        # self.update_time()

        # Сбрасываем текущий процесс и время начала
        self.current_process = None
        self.start_time = None
        # Сбрасываем общее время
        self.total_time = 0
        #TODO: Отправлять статистику в файл

        # Очищаем статистику
        self.processes = {}
        # self.wtrite_report()

        # Выводим сообщение о завершении считывания процессов
        message('Считывание процессов завершено', icon_path=None, title="Успешно")

    def time_apps_list(self, app_name):
        if app_name != self.current_process:
            print(self.processes)
        # Если приложение уже есть в словаре, то увеличиваем его время на 1 секунду
        if app_name in self.processes:
            self.processes[app_name] += 1
        # Иначе добавляем приложение в словарь с начальным временем 1 секунда
        else:
            self.processes[app_name] = 1

    def update(self):
        active_process = get_active_app_name()
        self.time_apps_list(active_process)
        self.current_process = get_active_app_name()


app = QApplication(sys.argv)
window = TimeTracker()
window.show()
sys.exit(app.exec())
