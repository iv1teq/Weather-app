from PyQt6 import QtWidgets as widgets
from PyQt6 import QtCore as core
from PyQt6.QtCore import pyqtSignal, Qt, QTimer
import datetime
import json

class Card (widgets.QFrame):
    clicked = pyqtSignal(object)
    def __init__(self, parent, city_name, temp, time, weather, min_temp, max_temp  ):
        super().__init__(parent)
        # self.CITY_NAME = city_name
        # self.TEMP = temp
        # self.TIME = time
        # self.WEATHER = weather
        # self.MAXMIN_TEMP = maxmin_temp
        self.LAYOUT_CARD = widgets.QGridLayout()


        self.setLayout(self.LAYOUT_CARD)
        self.CITY_NAME = widgets.QLabel( text = city_name )
        self.TEMP = widgets.QLabel( text = str(temp)+"°" )
        self.TIME = widgets.QLabel( text = str(time) )
        self.WEATHER = widgets.QLabel( text = str(weather) )
        self.MINMAX_TEMP = widgets.QLabel( text = str(f"min: {min_temp}°, max: {max_temp}°"))
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.CITY_NAME.setStyleSheet( "font-size: 30px; font-weight: bold; font: Roboto" )
        self.TEMP.setStyleSheet( "font-size: 44px; font-weight: bold; font: Roboto" )
        self.TIME.setStyleSheet( "font-size: 12px; font-weight: bold; font: Roboto" )
        self.WEATHER.setStyleSheet( "font-size: 12px; font-weight: bold; font: Roboto" )
        self.MINMAX_TEMP.setStyleSheet( "font-size: 12px; font-weight: bold; font: Roboto" )
        self.LAYOUT_CARD.setHorizontalSpacing(8)
        

        self.LAYOUT_CARD.addWidget(self.CITY_NAME, 1, 0, alignment = core.Qt.AlignmentFlag.AlignCenter)
        self.LAYOUT_CARD.addWidget(self.TEMP, 1, 2, 2, 2, alignment = core.Qt.AlignmentFlag.AlignRight)
        self.LAYOUT_CARD.addWidget(self.TIME, 2, 0, alignment = core.Qt.AlignmentFlag.AlignLeft | core.Qt.AlignmentFlag.AlignTop )
        self.LAYOUT_CARD.addWidget(self.WEATHER, 3, 0, alignment = core.Qt.AlignmentFlag.AlignLeft)
        self.LAYOUT_CARD.addWidget(self.MINMAX_TEMP, 3, 3, alignment = core.Qt.AlignmentFlag.AlignRight)
        self.city_name = city_name

        
    def update_time(self, ):
        with open(f"static/json/{self.city_name}.json", mode ="r") as file:
            data = json.load(file)
        curent_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(seconds=data["city"]["timezone"]))).strftime("%H:%M")
        self.TIME.setText(curent_time)
        
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self)

        






