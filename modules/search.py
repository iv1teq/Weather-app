import PyQt6.QtWidgets as widgets 
import PyQt6.QtCore as core
from PyQt6.QtCore import pyqtSignal


class Search (widgets.QLineEdit):
    city_entered = pyqtSignal(str)  # сигнал для отправки города родителю

    def __init__(self, parent ):
        super().__init__(parent)
        self.setObjectName('search')

        self.setStyleSheet('background-color: rgba(0, 0, 0, 60)')
        self.setFixedSize(core.QSize(200,50))
        self.returnPressed.connect(self.on_enter) 
        self.city = ''
        self.city.strip().lower().replace(" ", "")
    
    def on_enter(self):
            
        self.city = self.text()
        self.clear()
        self.city_entered.emit(self.city)  # уведомляем родителя
