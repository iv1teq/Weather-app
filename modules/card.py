from PyQt6 import QtWidgets as widgets
from PyQt6 import QtCore as core


class Card (widgets.QFrame):
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
        self.TEMP = widgets.QLabel( text = str(temp) )
        self.TIME = widgets.QLabel( text = str(temp) )
        self.WEATHER = widgets.QLabel( text = str(weather) )
        self.MINMAX_TEMP = widgets.QLabel( text = str(f"{min_temp} {max_temp}"))
        
        self.CITY_NAME.setStyleSheet( "font-size: 30px; font-weight: bold; font: Roboto" )
        self.TEMP.setStyleSheet( "font-size: 44px; font-weight: bold; font: Roboto" )
        self.TIME.setStyleSheet( "font-size: 12px; font-weight: bold; font: Roboto" )
        self.WEATHER.setStyleSheet( "font-size: 12px; font-weight: bold; font: Roboto" )
        self.MINMAX_TEMP.setStyleSheet( "font-size: 12px; font-weight: bold; font: Roboto" )
        

        self.LAYOUT_CARD.addWidget(self.CITY_NAME, 1, 1, alignment = core.Qt.AlignmentFlag.AlignLeft)
        self.LAYOUT_CARD.addWidget(self.TEMP, 1, 2, 2, 2, alignment = core.Qt.AlignmentFlag.AlignRight)
        self.LAYOUT_CARD.addWidget(self.TIME, 2, 1, alignment = core.Qt.AlignmentFlag.AlignTop)
        self.LAYOUT_CARD.addWidget(self.WEATHER, 3, 1, alignment = core.Qt.AlignmentFlag.AlignLeft)
        self.LAYOUT_CARD.addWidget(self.MINMAX_TEMP, 3, 3, alignment = core.Qt.AlignmentFlag.AlignRight)
        
        






