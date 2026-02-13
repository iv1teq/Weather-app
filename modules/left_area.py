from PyQt6 import QtWidgets as widgets
from PyQt6 import QtCore as core 
from PyQt6 import QtGui as gui
from PyQt6.QtGui import QIcon
from .card import Card



class LeftArea(widgets.QFrame):
    def __init__(self, parent: None, window_width: int, window_height: int ):
        super().__init__(parent)

        self.setFixedWidth(window_width)
        self.setFixedHeight(window_height)
        
        
        self.setStyleSheet("background-color: rgba(0, 0, 0, 50);")

        layout = widgets.QVBoxLayout(self)
        layout.setAlignment(core.Qt.AlignmentFlag.AlignCenter)


        self.button = widgets.QPushButton(parent= self)
        self.button.setIcon(QIcon("media/dark.png"))
        self.button.setFixedSize(core.QSize(70,50))
        self.button.setIconSize(core.QSize(70, 50))
        self.button.clicked.connect(self.icon_change)
        self.button.setStyleSheet("""
    background-color: transparent;  
    border: none;                   
    padding: 0px;                   
""")
        layout.addWidget(self.button, alignment=core.Qt.AlignmentFlag.AlignRight)
        self.BUTTON_PRESSED = False

        
        self.scroll_area = widgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        self.scroll_area.setStyleSheet("""
    background-color: transparent;  
    border: none;                   
""")
        
        self.scroll_area.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_frame = widgets.QFrame()
        self.scroll_layout = widgets.QVBoxLayout(self.scroll_frame)

        self.scroll_area.setWidget(self.scroll_frame)
        layout.addWidget(self.scroll_area)

    def add_card(self, card_width:float):
        for _ in range(10):

            card = Card(self.scroll_frame)
            card1_width = card_width
            self.scroll_layout.addWidget(card, alignment = core.Qt.AlignmentFlag.AlignCenter)
            card.setFixedSize(core.QSize(int(card1_width), 100))
            card.setStyleSheet("""
QFrame {
    background-color: transparent;
    border-radius: 12px;
}

QFrame:hover {
    background-color: rgba(255, 255, 255, 30);
}
QLabel{
    background-color: transparent;                         
}
QLabel:hover{
    background-color: None;                         
}
""")





    def icon_change(self):
        if self.BUTTON_PRESSED == False:
            self.button.setIcon(QIcon("media/light.png"))
            self.BUTTON_PRESSED = True
            

        elif self.BUTTON_PRESSED == True:
            self.button.setIcon(QIcon("media/dark.png"))
            self.BUTTON_PRESSED = False





