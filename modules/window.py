import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets

from .app import app_obj
from .title_bar import Title_bar
from utils import api_request
from .left_area import LeftArea
from .hour_forecast import Hour_forecast
from .search import Search
import sys
from .right_area import RightArea
from .search import Search
from .card import Card
import json
from utils import api_request 

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


class MainWindow(widgets.QMainWindow):
        
        def __init__(self, window_width: int, window_height: int):
                widgets.QMainWindow.__init__(self)
                

                self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)
                
                self.WINDOW_WIDTH = window_width
                self.WINDOW_HEIGHT = window_height
                #search obj
                self.SEARCH = Search(self)
                #file open
                
                
        
                #card obj
                self.CARD = Card ( parent = None ,
                                city_name = None, 
                                temp = None , 
                                time = None, 
                                weather = None, 
                                min_temp = None, 
                                max_temp = None, 
                                main_window=self, 
                                search=self.SEARCH,
                                )
                
                
                
                self.SCREEN = app_obj.primaryScreen()
                self.SCREEN_SIZE = self.SCREEN.size()
                
                self.SCREEN_WIDTH = self.SCREEN_SIZE.width()
                self.SCREEN_HEIGHT = self.SCREEN_SIZE.height()
                
                self.CENTER_X = (self.SCREEN_WIDTH // 2) - (self.WINDOW_WIDTH // 2)
                self.CENTER_Y = (self.SCREEN_HEIGHT // 2) - (self.WINDOW_HEIGHT // 2)
                
                # self.setGeometry(self.CENTER_X, self.CENTER_Y, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
                self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
                self.move(self.CENTER_X, self.CENTER_Y)
                
                # Делает фон всего окна прозрачным, чтобы закругление было видно
                self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)

        # Центральный виджет 
                self.CENTRAL_WIDGET = widgets.QWidget(parent=self)
                self.setCentralWidget(self.CENTRAL_WIDGET)
                self.CENTRAL_WIDGET.setStyleSheet("""
        QWidget {
        background-color: white;   
        border-radius: 10px;       
        }
        """)

        # Настройка центрального виджета
                self.CENTRAL_WIDGET_LAYOUT = widgets.QVBoxLayout()
                self.CENTRAL_WIDGET_LAYOUT.setContentsMargins(0, 0, 0, 0)
                self.CENTRAL_WIDGET_LAYOUT.setSpacing(0)
                self.CENTRAL_WIDGET.setLayout(self.CENTRAL_WIDGET_LAYOUT)

        # TITLE_BAR добавляем в центральный виджет
                self.TITLE_BAR = Title_bar(self.CENTRAL_WIDGET, width=self.WINDOW_WIDTH)
                self.CENTRAL_WIDGET_LAYOUT.addWidget(self.TITLE_BAR)
        # self.WINDOW_WIDTH, content_frame_height)
        # CONTENT_FRAME — все окно без titlebar
                self.CONTENT_FRAME = widgets.QFrame(self.CENTRAL_WIDGET)
                self.CONTENT_FRAME.setSizePolicy(widgets.QSizePolicy.Policy.Expanding, widgets.QSizePolicy.Policy.Expanding)
                self.CONTENT_FRAME_LAYOUT = widgets.QHBoxLayout()
                self.CONTENT_FRAME_LAYOUT.setContentsMargins(0, 0, 0, 0)
                self.CONTENT_FRAME_LAYOUT.setSpacing(0)
                self.CONTENT_FRAME.setLayout(self.CONTENT_FRAME_LAYOUT)
                #Right Area
                self.RIGHTAREA = RightArea(self.CONTENT_FRAME, search = self.SEARCH, card = self.CARD, main_window=self)
                self.RIGHTAREA.setSizePolicy(
        widgets.QSizePolicy.Policy.Expanding,
        widgets.QSizePolicy.Policy.Expanding
        )


        # LeftArea внутри CONTENT_FRAME 
                self.LEFTAREA = LeftArea(self.CONTENT_FRAME, 
                                        search=self.SEARCH,
                                        card = Card, 
                                        main_window = self
                                        )
                
                #connect
                # self.SEARCH.city_entered.connect(self.entered(city = self.SEARCH.city, left_area = self.LEFTAREA))
                
                self.SEARCH.city_entered.connect(
                lambda: self.entered(city=self.SEARCH.city, left_area = self.LEFTAREA, card = self.CARD)
)                       
                
        # Добавляем LEFTAREA в CONTENT_FRAME
                self.CONTENT_FRAME_LAYOUT.addWidget(self.LEFTAREA, 1 )
                self.CONTENT_FRAME_LAYOUT.addWidget(self.RIGHTAREA, 2)
                self.CONTENT_FRAME_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignLeft)

        # Фон CONTENT_FRAME — градиент, углы 
                self.CONTENT_FRAME.setStyleSheet("""
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

        # Добавляем CONTENT_FRAME в центральный виджет

                self.CENTRAL_WIDGET_LAYOUT.addWidget(self.CONTENT_FRAME)
                
        def entered(self, city , left_area, card):

                self.data = api_request(city)

                left_area.update_data(self.data)
                card.update_data(self.data, main_window=self)

                
        def card_clicked(self):

                self.RIGHTAREA.update_data(data = self.data)

                        
        
        


        














