from PyQt6 import QtWidgets as widgets
from PyQt6 import QtCore as core
from PyQt6.QtCore import pyqtSignal, Qt, QTimer
import datetime
import json

class Card (widgets.QFrame):
    clicked = pyqtSignal(object)
    delete_requested = pyqtSignal(object)
    def __init__(self, parent, city_name, temp, time, weather, min_temp, max_temp,  main_window , search):
        super().__init__(parent)
        self.setObjectName("card")
        # self.LAYOUT_CARD = widgets.QGridLayout()
        # self.LAYOUT_CARD.setSpacing(0)
        self.main_window = main_window
        self.search = search
        self.data = None
        #card layout
        self.icon_city_layout = widgets.QHBoxLayout()
        self.icon_city_layout.setContentsMargins(0,0,0,0)
        self.icon_city_layout.setSpacing(15)
        
        self.main_layout = widgets.QVBoxLayout()
        self.left_right_layout = widgets.QHBoxLayout()
        self.left_layout = widgets.QVBoxLayout()
        self.right_layout = widgets.QVBoxLayout()
        
        self.setMinimumWidth(int(main_window.width() / 5))

        self.left_layout.addLayout(self.icon_city_layout)
        
        self.left_right_layout.addLayout(self.left_layout)
        self.left_right_layout.addLayout(self.right_layout)
        self.main_layout.addLayout(self.left_right_layout)

        self.setLayout(self.main_layout)
        self.CITY_NAME = widgets.QLabel( text = city_name )
        self.TEMP = widgets.QLabel( text = str(temp)+"°" )
        self.TIME = widgets.QLabel( text = str(time) )
        self.WEATHER = widgets.QLabel( text = str(weather) )
        self.MINMAX_TEMP = widgets.QLabel( text = str(f"min: {min_temp}°, max: {max_temp}°"))

        self.timer = QTimer()
        if  self.search.city != '':
            self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.CITY_NAME.setStyleSheet( "font-size: 40px; font-weight: bold; font: Roboto;" )
        self.TEMP.setStyleSheet( "font-size: 60px; font-weight: bold; font: Roboto" )
        self.TIME.setStyleSheet( "font-size: 20px; font-weight: bold; font: Roboto" )
        self.WEATHER.setStyleSheet( "font-size: 20px; font-weight: bold; font: Roboto" )
        self.MINMAX_TEMP.setStyleSheet( "font-size: 20px; font-weight: bold; font: Roboto" )

        self.underline = widgets.QFrame()
        self.underline.setFixedSize(int((main_window.width() / 3)- (main_window.width() / 250 )), 5)  # размер контейнера
        self.underline.setStyleSheet("background: none; padding-bottom: 5px; border-bottom: 2px solid rgba(255, 255, 255, 50);")



        
        self.icon_city_layout.addWidget(self.CITY_NAME)
        self.right_layout.addWidget(self.TEMP, alignment = core.Qt.AlignmentFlag.AlignRight)
        self.left_layout.addWidget(self.TIME)
        self.left_layout.addWidget(self.WEATHER)
        self.right_layout.addWidget(self.MINMAX_TEMP, alignment = core.Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(self.underline)
        self.city_name = city_name
        

        
    def update_time(self): 
        if self.data:
            curent_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(seconds=self.data["city"]["timezone"]))).strftime("%H:%M")
            self.TIME.setText(curent_time)
        
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self)


        
    def update_data(self, data, main_window):
        self.data = data
        self.underline.setFixedSize(int(main_window.width() / 3 - 80), 5)







