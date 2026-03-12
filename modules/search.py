import PyQt6.QtWidgets as widgets 
import PyQt6.QtCore as core
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPixmap


class Search (widgets.QLineEdit):
    city_entered = pyqtSignal(str)  # сигнал для отправки города родителю

    def __init__(self, parent ):
        super().__init__(parent)

        self.setObjectName('search')
        self.setStyleSheet('background-color: rgba(0, 0, 0, 0)')
        self.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding )
        self.returnPressed.connect(self.on_enter) 
        self.city = ''
        self.city.strip().lower().replace(" ", "")
        self.setPlaceholderText("search")
    def on_enter(self):
        self.city = self.text()
        self.clear()
        self.city_entered.emit(self.city)  # уведомляем родителя
