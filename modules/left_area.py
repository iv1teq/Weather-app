from PyQt6 import QtWidgets as widgets
from PyQt6 import QtCore as core 
from PyQt6 import QtGui as gui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from .card import Card
from .search import Search
from static import json
import json
import datetime
from utils import api_request
from PyQt6.QtGui import QPixmap

class LeftArea(widgets.QFrame):
    def __init__(self, parent: None, main_window ):
        super().__init__(parent)
        self.main_window = main_window
        

        self.setSizePolicy(widgets.QSizePolicy.Policy.Preferred, widgets.QSizePolicy.Policy.Expanding)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 50);")

        #vertikal layout
        layout = widgets.QVBoxLayout(self)

        #horizontal layout top
        top_layout = widgets.QHBoxLayout()
        top_layout.setSpacing(0)

        #layouts toogether
        layout.addLayout(top_layout)

        #search object
        self.search_obj = Search(parent = self)
        top_layout.addWidget(self.search_obj)
        self.search_obj.city_entered.connect(self.handle_city)

        

        

        #theme button
        self.button = widgets.QPushButton(parent= self)
        self.button.setIcon(QIcon("media/light.png"))
        self.button.setIconSize(core.QSize(50, 50))  # базовый размер иконки
        self.button.setMinimumSize(50, 50)   
        self.button.clicked.connect(self.icon_change)
        self.button.setSizePolicy(
    widgets.QSizePolicy.Policy.MinimumExpanding,  # ширина растягивается, но минимальная = fixed
    widgets.QSizePolicy.Policy.Fixed             # высота фиксирована
)
        #Стили
        self.button.setStyleSheet("""
    background-color: transparent;  
    border: none;                   
    padding: 0px;                   
""")
        top_layout.addWidget(self.button, alignment=core.Qt.AlignmentFlag.AlignRight)
        self.BUTTON_PRESSED = False

        #scroll
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
        self.scroll_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setContentsMargins(5,5,5,5)
        self.scroll_layout.setSpacing(10)
        self.scroll_frame.setSizePolicy(widgets.QSizePolicy.Policy.Expanding, widgets.QSizePolicy.Policy.Expanding)

        self.scroll_area.setWidget(self.scroll_frame)
        layout.addWidget(self.scroll_area)
        
        #флаг для карточки где мы
        self.active_card = None 
        self.active_image = None 
    # cards with forecast
    def add_card(self, city=None):
        if city is None:
            city = self.search_obj.city 
        with open(f"static/json/{self.search_obj.city}.json", mode ="r") as file:
            self.DATA = json.load(file)
            if "list" not in self.DATA :
                self.search_obj.city = ''
                self.search_obj.clear()
                return
            else:
                card = Card(self.scroll_frame, 
                            city_name = self.search_obj.city, 
                            temp = round(self.DATA["list"][0]["main"]["temp"]), 
                            time = datetime.datetime.now(datetime.timezone(datetime.timedelta(seconds=self.DATA["city"]["timezone"]))).strftime("%H:%M"),
                            weather = self.DATA["list"][0]["weather"][0]["description"], 
                            min_temp=round(self.DATA["list"][0]["main"]["temp_min"]),
                            max_temp=round(self.DATA["list"][0]["main"]["temp_max"]))
                card.clicked.connect(self.add_image)
                self.scroll_layout.addWidget(card)
                card.setFixedHeight(100)
                card.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Fixed
        )
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




#icon change for button
    def icon_change(self):
        if self.BUTTON_PRESSED == False:
            from .window import MainWindow
            self.button.setIcon(QIcon("media/dark.png"))
            self.main_window.CONTENT_FRAME.setStyleSheet("""
QFrame {
    background: qlineargradient(
        x1:0, y1:1,        
        x2:1, y2:0,        
        stop:0 #464649,      
        stop:1 #464649 
    );
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px; 
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}
""")


            self.BUTTON_PRESSED = True

            

        elif self.BUTTON_PRESSED == True:
            self.button.setIcon(QIcon("media/light.png"))
            self.BUTTON_PRESSED = False
            self.main_window.CONTENT_FRAME.setStyleSheet("""
QFrame {
    background: qlineargradient(
        x1:0, y1:1,        
        x2:1, y2:0,        
        stop:0 #87CEFA,      
        stop:1 #FFDF56 
    );
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px; 
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}
""")

    def handle_city(self, city):
        from utils import api_request 
        api_request(city)  # создаёт JSON
        self.add_card(city=city) #activate add card


    def add_image(self,card):
        if self.active_image is None :
            self.active_image = widgets.QLabel()
            pix_map = QPixmap('media/Vector.png')
            self.active_image.setPixmap(pix_map)
            
        
        if self.active_card is not None:
            card.LAYOUT_CARD.removeWidget(self.active_image)
        
        card.LAYOUT_CARD.addWidget(self.active_image, 1, 0, alignment = core.Qt.AlignmentFlag.AlignLeft)
        self.active_card = card




