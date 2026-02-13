from PyQt6 import QtWidgets as widgets
from PyQt6 import QtCore as core


class Card (widgets.QFrame):
    def __init__(self, parent = None ):
        super().__init__(parent)

        self.LAYOUT_CARD = widgets.QGridLayout()


        self.setLayout(self.LAYOUT_CARD)
        self.CITY_NAME = widgets.QLabel( text = "name")
        self.TEMP = widgets.QLabel( text = "temp")
        self.TIME = widgets.QLabel( text = "time")
        self.CONDITION = widgets.QLabel( text = "condition")
        self.MAXMIN_TEMP = widgets.QLabel( text = "max, min")
        self.CITY_NAME.setStyleSheet("font-size: 30px; font-weight: bold; font: Roboto")
        self.TEMP.setStyleSheet("font-size: 44px; font-weight: bold; font: Roboto")
        self.TIME.setStyleSheet("font-size: 12px; font-weight: bold; font: Roboto")
        self.CONDITION.setStyleSheet("font-size: 12px; font-weight: bold; font: Roboto")
        self.MAXMIN_TEMP.setStyleSheet("font-size: 12px; font-weight: bold; font: Roboto")
        

        self.LAYOUT_CARD.addWidget(self.CITY_NAME, 1, 1, alignment = core.Qt.AlignmentFlag.AlignLeft)
        self.LAYOUT_CARD.addWidget(self.TEMP, 1, 2, 2, 2, alignment = core.Qt.AlignmentFlag.AlignRight)
        self.LAYOUT_CARD.addWidget(self.TIME, 2, 1, alignment = core.Qt.AlignmentFlag.AlignTop)
        self.LAYOUT_CARD.addWidget(self.CONDITION, 3, 1, alignment = core.Qt.AlignmentFlag.AlignLeft)
        self.LAYOUT_CARD.addWidget(self.MAXMIN_TEMP, 3, 3, alignment = core.Qt.AlignmentFlag.AlignRight)
        
        






