import os
import datetime

from PyQt6 import QtWidgets as widgets
from PyQt6 import QtCore as core
from PyQt6.QtGui import QIcon, QPixmap

from .card import Card
from .search import Search
from utils import api_request


class LeftArea(widgets.QFrame):

    CARD_STYLE_DEFAULT = """
        QFrame#card {
            background-color: transparent;
            border-radius: 12px;
        }
        QFrame#card:hover {
            background-color: rgba(0, 0, 0, 30);
        }
        QLabel {
            background-color: transparent;
        }
    """

    CARD_STYLE_ACTIVE = """
        QFrame#card {
            background-color: rgba(0, 0, 0, 30);
            border-radius: 12px;
        }
        QFrame#card:hover {
            background-color: rgba(0, 0, 0, 30);
        }
        QLabel {
            background-color: transparent;
        }
    """

    def __init__(self, parent, search, card, main_window, card_list, deleted_card_list):
        super().__init__(parent)
        self.setObjectName('left_area')

        self.main_window = main_window
        self.search = search
        self.CardClass = card
        self.data = None
        self.card_list = card_list
        self.deleted_card_list = deleted_card_list
        self.active_card = None
        self.BUTTON_PRESSED = False

        self._setup_widget()
        self._setup_theme_button()
        self._setup_scroll_area()

    # ИНИЦИАЛИЗАЦИЯ

    def _setup_widget(self):
        self.setSizePolicy(
            widgets.QSizePolicy.Policy.Preferred,
            widgets.QSizePolicy.Policy.Expanding,
        )
        self.setMaximumWidth(int(self.main_window.width() / 3))
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100); border-radius: 0px;")

        self.main_layout = widgets.QVBoxLayout(self)
        self.top_layout = widgets.QHBoxLayout()
        self.top_layout.setSpacing(0)
        self.main_layout.addLayout(self.top_layout)

    def _setup_theme_button(self):
        self.button = widgets.QPushButton(parent=self)
        self.button.setIcon(QIcon("media/dark.png"))
        self.button.setIconSize(core.QSize(50, 50))
        self.button.setMinimumSize(50, 50)
        self.button.setStyleSheet("background-color: transparent; border: none; padding: 0px;")
        self.button.setSizePolicy(
            widgets.QSizePolicy.Policy.MinimumExpanding,
            widgets.QSizePolicy.Policy.Fixed,
        )
        self.button.clicked.connect(self.icon_change)
        self.top_layout.addWidget(self.button, alignment=core.Qt.AlignmentFlag.AlignRight)

    def _setup_scroll_area(self):
        self.scroll_area = widgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: transparent; border: none;")
        self.scroll_area.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll_frame = widgets.QFrame()
        self.scroll_frame.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Expanding,
        )

        self.scroll_layout = widgets.QVBoxLayout(self.scroll_frame)
        self.scroll_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_layout.setSpacing(10)

        self.scroll_area.setWidget(self.scroll_frame)
        self.main_layout.addWidget(self.scroll_area)

    # КАРТОЧКИ

    def add_card(self):
        if self.data is None:
            return

        if "list" not in self.data:
            os.remove(f"static/json/{self.search.city}.json")
            self.search.city = ''
            self.search.clear()
            return

        self.card_list.append(self.search.city)
        tz = datetime.timezone(datetime.timedelta(seconds=self.data["city"]["timezone"]))

        self.card = self.CardClass(
            self.scroll_frame,
            city_name=self.search.city,
            temp=round(self.data["list"][0]["main"]["temp"]),
            time=datetime.datetime.now(tz).strftime("%H:%M"),
            # weather — описание с API, не переводится через tr(),
            # это данные от сервера (английский текст OpenWeatherMap)
            weather=self.data["list"][0]["weather"][0]["description"],
            min_temp=round(self.data["list"][0]["main"]["temp_min"]),
            max_temp=round(self.data["list"][0]["main"]["temp_max"]),
            main_window=self.main_window,
            search=self.search,
        )
        self.card.data = self.data
        self.card.setMinimumHeight(150)
        self.card.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Fixed,
        )
        self.card.setStyleSheet(self.CARD_STYLE_DEFAULT)

        self.scroll_layout.insertWidget(0, self.card)
        self.card.clicked.connect(self.change_card_bg)
        self.card.clicked.connect(self.main_window.card_clicked)
        self.card.delete_requested.connect(self.remove_card)

    def remove_card(self, card):
        card.timer.stop()
        if card.city_name in self.card_list:
            self.card_list.remove(card.city_name)
        if self.active_card is card:
            self.active_card = None
        self.scroll_layout.removeWidget(card)
        card.deleteLater()

    def remove_card_by_name(self, city_name):
        for i in range(self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i)
            if item and item.widget():
                card = item.widget()
                if card.city_name == city_name:
                    card.timer.stop()
                    if self.active_card is card:
                        self.active_card = None
                    self.scroll_layout.removeWidget(card)
                    card.deleteLater()
                    break

    def change_card_bg(self, card):
        if self.active_card is not None and self.active_card is not card:
            self.active_card.setStyleSheet(self.CARD_STYLE_DEFAULT)

        card.setStyleSheet(self.CARD_STYLE_ACTIVE)
        self.active_card = card

        if card.data and "city" in card.data:
            lat = card.data["city"]["coord"]["lat"]
            lon = card.data["city"]["coord"]["lon"]
            self.main_window.RIGHTAREA.SETTINGS.update_map(lat, lon)

    def update_data(self, data):
        self.data = data
        self.add_card()

    # СМЕНА ТЕМЫ

    def icon_change(self):
        if not self.BUTTON_PRESSED:
            self.button.setIcon(QIcon("media/light.png"))
            self.main_window.CENTRAL_WIDGET.setStyleSheet("""
                QWidget {
                    background: qlineargradient(
                        x1:0, y1:1, x2:1, y2:0,
                        stop:0 #87CEFA, stop:1 #FFDF56
                    );
                    border-radius: 10px;
                }
            """)
            self.main_window.CONTENT_FRAME.setStyleSheet("""
                QFrame {
                    background: qlineargradient(
                        x1:0, y1:1, x2:1, y2:0,
                        stop:0 #87CEFA, stop:1 #FFDF56
                    );
                    border-bottom-left-radius: 10px;
                    border-bottom-right-radius: 10px;
                    border-top-left-radius: 0px;
                    border-top-right-radius: 0px;
                }
            """)
            self.BUTTON_PRESSED = True
        else:
            self.button.setIcon(QIcon("media/dark.png"))
            self.main_window.CENTRAL_WIDGET.setStyleSheet("""
                QWidget {
                    background: qlineargradient(
                        x1:0, y1:1, x2:1, y2:0,
                        stop:0 #5DADE2, stop:1 #808080
                    );
                    border-radius: 10px;
                }
            """)
            self.main_window.CONTENT_FRAME.setStyleSheet("""
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
            self.BUTTON_PRESSED = False

    # ПЕРЕВОДЫ

    def retranslateUi(self):
        # Переводим все карточки в scroll_layout
        for i in range(self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i)
            if item and item.widget():
                card = item.widget()
                # Карточка должна реализовать retranslateUi() у себя
                if hasattr(card, 'retranslateUi'):
                    card.retranslateUi()

    def changeEvent(self, event):
        if event.type() == core.QEvent.Type.LanguageChange:
            self.retranslateUi()
        super().changeEvent(event)