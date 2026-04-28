import sys
import json

import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets

from .app import app_obj
from .title_bar import Title_bar
from .left_area import LeftArea
from .right_area import RightArea
from .search import Search
from .card import Card
from utils import api_request

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# class Central_widget():
#     def __init__(self, parent, leng):
        
#         label_ukr = widgets.QLabel(text ='Привіт')
#         label_eng = widgets.QLabel(text ='Hello')



#         dict = {'eng': label_eng,
#                 'ukr': label_ukr}
        
#         dict[leng]

class MainWindow(widgets.QMainWindow):

    def __init__(self, window_width: int, window_height: int):
        widgets.QMainWindow.__init__(self)

        self.WINDOW_WIDTH = window_width
        self.WINDOW_HEIGHT = window_height

        self.card_list = []
        self.deleted_card_list = []

        self._setup_window()
        self._setup_central_widget()
        self._setup_content()
        self._connect_signals()

    # ИНИЦИАЛИЗАЦИЯ

    def _setup_window(self):
        # убираем стандартную рамку окна
        self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)

        # центрируем окно на экране
        screen = app_obj.primaryScreen().size()
        self.SCREEN_WIDTH = screen.width()
        self.SCREEN_HEIGHT = screen.height()
        center_x = (self.SCREEN_WIDTH // 2) - (self.WINDOW_WIDTH // 2)
        center_y = (self.SCREEN_HEIGHT // 2) - (self.WINDOW_HEIGHT // 2)

        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.move(center_x, center_y)

        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:1, x2:1, y2:0,
                    stop:0 #5DADE2, stop:1 #808080
                );
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
            }
        """)

    def _setup_central_widget(self):
        self.CENTRAL_WIDGET = widgets.QWidget(parent=self)
        self.CENTRAL_WIDGET.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:1, x2:1, y2:0,
                    stop:0 #5DADE2, stop:1 #808080
                );
                border-radius: 10px;
            }
        """)

        self.CENTRAL_WIDGET_LAYOUT = widgets.QVBoxLayout()
        self.CENTRAL_WIDGET_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.CENTRAL_WIDGET_LAYOUT.setSpacing(0)
        self.CENTRAL_WIDGET.setLayout(self.CENTRAL_WIDGET_LAYOUT)
        self.setCentralWidget(self.CENTRAL_WIDGET)

        # title bar
        self.TITLE_BAR = Title_bar(self.CENTRAL_WIDGET, width=self.WINDOW_WIDTH)
        self.CENTRAL_WIDGET_LAYOUT.addWidget(self.TITLE_BAR)

    def _setup_content(self):
        # основная область под title bar
        self.CONTENT_FRAME = widgets.QFrame(self.CENTRAL_WIDGET)
        self.CONTENT_FRAME.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Expanding
        )
        self.CONTENT_FRAME.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:1, x2:1, y2:0,
                    stop:0 #5DADE2, stop:1 #808080
                );
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
            }
        """)

        self.CONTENT_FRAME_LAYOUT = widgets.QHBoxLayout()
        self.CONTENT_FRAME_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.CONTENT_FRAME_LAYOUT.setSpacing(0)
        self.CONTENT_FRAME.setLayout(self.CONTENT_FRAME_LAYOUT)

        # объекты поиска и карточки
        self.SEARCH = Search(self)
        self.CARD = Card(
            parent=None,
            city_name=None,
            temp=None,
            time=None,
            weather=None,
            min_temp=None,
            max_temp=None,
            main_window=self,
            search=self.SEARCH,
        )

        # левая панель
        self.LEFTAREA = LeftArea(
            self.CONTENT_FRAME,
            search=self.SEARCH,
            card=Card,
            main_window=self,
            card_list=self.card_list,
            deleted_card_list=self.deleted_card_list,
        )
        self.LEFTAREA.setMinimumWidth(self.WINDOW_WIDTH // 3)
        self.LEFTAREA.setSizePolicy(
            widgets.QSizePolicy.Policy.Fixed,
            widgets.QSizePolicy.Policy.Expanding,
        )

        # правая панель
        self.RIGHTAREA = RightArea(
            self.CONTENT_FRAME,
            search=self.SEARCH,
            card=self.CARD,
            content_frame=self.CONTENT_FRAME,
            main_window=self,
            card_list=self.card_list,
            deleted_card_list=self.deleted_card_list,
            left_area=self.LEFTAREA,
            window_height=self.WINDOW_HEIGHT,
            window_width=self.WINDOW_WIDTH,
        )
        self.RIGHTAREA.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Expanding,
        )

        self.CONTENT_FRAME_LAYOUT.addWidget(self.LEFTAREA, 1)
        self.CONTENT_FRAME_LAYOUT.addWidget(self.RIGHTAREA, 2)
        self.CONTENT_FRAME_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignLeft)

        self.CENTRAL_WIDGET_LAYOUT.addWidget(self.CONTENT_FRAME)

    def _connect_signals(self):
        self.SEARCH.city_entered.connect(
            lambda: self.entered(city=self.SEARCH.city, left_area=self.LEFTAREA, card=self.CARD)
        )

    # ЛОГИКА

    def entered(self, city, left_area, card):
        # запрос погоды и обновление виджетов
        self.data = api_request(city)
        left_area.update_data(self.data)
        card.update_data(self.data, main_window=self)

    def card_clicked(self, card):
        # пересоздаём правую панель при клике на карточку
        self.data = card.data
        self.CONTENT_FRAME_LAYOUT.removeWidget(self.RIGHTAREA)
        self.RIGHTAREA.deleteLater()

        self.RIGHTAREA = RightArea(
            self.CONTENT_FRAME,
            search=self.SEARCH,
            card=card,
            content_frame=self.CONTENT_FRAME,
            main_window=self,
            card_list=self.card_list,
            deleted_card_list=self.deleted_card_list,
            window_width=self.WINDOW_WIDTH,
            window_height=self.WINDOW_HEIGHT,
            left_area=self.LEFTAREA,
        )
        self.RIGHTAREA.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Expanding,
        )

        self.CONTENT_FRAME_LAYOUT.addWidget(self.RIGHTAREA, 2)
        self.RIGHTAREA.update_data(data=self.data)
