from PyQt6 import QtWidgets as widgets
from PyQt6 import QtCore as core 

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from .card import Card
from .search import Search
from static import json
import json
import datetime
from utils import api_request
from PyQt6.QtGui import QPixmap
import os 
from PyQt6.QtCore import Qt




class LeftArea(widgets.QFrame):
    def __init__(self, parent: None, search, card , main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.search = search
        self.CardClass = card
        self.main_window = main_window
        self.data = None
        


        self.setSizePolicy(widgets.QSizePolicy.Policy.Preferred, widgets.QSizePolicy.Policy.Expanding)
        self.setMaximumWidth(int(main_window.width()/3))
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100); border-radius: 0px;")

        #vertikal layout
        layout = widgets.QVBoxLayout(self)

        #horizontal layout top
        top_layout = widgets.QHBoxLayout()
        top_layout.setSpacing(0)


        #layouts toogether
        layout.addLayout(top_layout)

        #search object

        # top_layout.addWidget(self.search)
        

        #theme button
        self.button = widgets.QPushButton(parent = self)
        self.button.setIcon(QIcon("media/dark.png"))
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
        self.scroll_area.setStyleSheet("border-radius: 0px;")
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

    CARD_STYLE_DEFAULT = """
    QFrame {
        background-color: transparent;
        border-radius: 12px;
    }
    QFrame:hover {
        background-color: rgba(0, 0, 0, 30);
    }
    QLabel {
        background-color: transparent;
    }
    QLabel:hover {
        background-color: None;
    }
    """

    CARD_STYLE_ACTIVE = """
    QFrame {
        background-color: rgba(0, 0, 0, 30);
        border-radius: 12px;
    }
    QFrame:hover {
        background-color: rgba(0, 0, 0, 30);
    }
    QLabel {
        background-color: transparent;
    }
    QLabel:hover {
        background-color: None;
    }
    """

    # cards with forecast
    def add_card(self):
        if self.data is None:
            return
        if "list" not in self.data :
            os.remove(f"static/json/{self.search.city}.json")
            self.search.city = ''
            self.search.clear()
            return
        else:
            self.card = self.CardClass(self.scroll_frame, 
                        city_name = self.search.city, 
                        temp = round(self.data["list"][0]["main"]["temp"]), 
                        time = datetime.datetime.now(datetime.timezone(datetime.timedelta(seconds=self.data["city"]["timezone"]))).strftime("%H:%M"),
                        weather = self.data["list"][0]["weather"][0]["description"], 
                        min_temp=round(self.data["list"][0]["main"]["temp_min"]),
                        max_temp=round(self.data["list"][0]["main"]["temp_max"]),
                        main_window = self.main_window, 
                        search = self.search)
            self.card.data = self.data
            self.scroll_layout.insertWidget(0, self.card)
            self.card.setMinimumHeight(150)
            self.card.setSizePolicy(
        widgets.QSizePolicy.Policy.Expanding,
        widgets.QSizePolicy.Policy.Fixed
    )
            self.card.setStyleSheet(self.CARD_STYLE_DEFAULT)

            # передаём саму карточку в обработчик
            self.card.clicked.connect(self.change_card_bg)
            self.card.clicked.connect(self.main_window.card_clicked)




#icon change for button
    def icon_change(self):
        if self.BUTTON_PRESSED == False:
            self.button.setIcon(QIcon("media/light.png"))
            self.main_window.CENTRAL_WIDGET.setStyleSheet("""
        QWidget {
        background: qlineargradient(
        x1:0, y1:1,        
        x2:1, y2:0,  
        stop:0 #87CEFA,      
        stop:1 #FFDF56
        ) ; 
        border-radius: 10px;    
        }
        """)
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

            self.BUTTON_PRESSED = True

            

        elif self.BUTTON_PRESSED == True:
            self.button.setIcon(QIcon("media/dark.png"))
            self.BUTTON_PRESSED = False
            self.main_window.CENTRAL_WIDGET.setStyleSheet("""
        QWidget {
        background: qlineargradient(
        x1:0, y1:1,        
        x2:1, y2:0,  
        stop:0 #5DADE2,      
        stop:1 #808080 
        ) ; 
        border-radius: 10px;    
        }
        """)
            self.main_window.CONTENT_FRAME.setStyleSheet("""
QFrame {
    background: qlineargradient(
        x1:0, y1:1,        
        x2:1, y2:0,  
        stop:0 #5DADE2,      
        stop:1 #808080                                                      

    );
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px; 
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}
""")


    def change_card_bg(self, card):
        # сбрасываем стиль у предыдущей активной карточки
        if self.active_card is not None and self.active_card is not card:
            self.active_card.setStyleSheet(self.CARD_STYLE_DEFAULT)

        # применяем затемнение к новой
        card.setStyleSheet(self.CARD_STYLE_ACTIVE)
        self.active_card = card
        
    def update_data(self, data):
        self.data = data
        self.add_card()