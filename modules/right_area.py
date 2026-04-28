import datetime

import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from .search import Search
from .hour_forecast import Hour_forecast
from .forecast12h import Forecast12
from .combo_box import Search_listwidget
from .settings import Settings


class RightArea(widgets.QFrame):

    def __init__(self, parent, search, card, content_frame, main_window,
                 card_list, deleted_card_list, left_area, window_width, window_height):
        super().__init__(parent)
        self.setObjectName('right_area')

        self.content_frame = content_frame
        self.data = None
        self.search = search
        self.card = card
        self.card_list = card_list
        self.deleted_card_list = deleted_card_list
        self.left_area = left_area
        self.window_height = window_height
        self.window_width = window_width

        self.left_arrow_pressed_flag = True
        self.right_arrow_pressed_flag = False

        # Храним данные для retranslateUi
        self._min = None
        self._max = None

        self._setup_settings(main_window)
        self._setup_layouts()
        self._setup_top_frames(main_window)
        self._setup_left_content()
        self._setup_right_content()
        self._setup_header()
        self._setup_search_widget()
        self._setup_bottom_widgets()

        self.retranslateUi()

    # ИНИЦИАЛИЗАЦИЯ

    def _setup_settings(self, main_window):
        self.SETTINGS = Settings(
            parent=main_window,
            content_frame=self.content_frame,
            search=self.search,
            card_list=self.card_list,
            deleted_card_list=self.deleted_card_list,
            left_area=self.left_area,
            window_height=self.window_height,
            window_width=self.window_width,
        )
        self.SETTINGS.move(450, 100)
        self.SETTINGS.setStyleSheet("border-radius: 10px; background: #333333;")
        self.SETTINGS.hide()

    def _setup_layouts(self):
        self.LAYOUT = widgets.QGridLayout()
        self.LAYOUT.setRowStretch(2, 1)
        self.LAYOUT.setRowStretch(3, 1)
        self.LAYOUT.setColumnStretch(0, 1)
        self.LAYOUT.setColumnStretch(1, 1)
        self.LAYOUT.setContentsMargins(10, 10, 10, 10)
        self.LAYOUT.setSpacing(10)
        self.setLayout(self.LAYOUT)

        self.HEADER_LAYOUT = widgets.QHBoxLayout()
        self.LEFT_LAYOUT = widgets.QVBoxLayout()
        self.RIGHT_LAYOUT = widgets.QVBoxLayout()
        self.RIGHT_LAYOUT.setSpacing(10)
        self.TOP_LAYOUT = widgets.QHBoxLayout()
        self.TOP_LAYOUT.setSpacing(0)
        self.TOP_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        self.ICON_TEMP_LAYOUT = widgets.QHBoxLayout()
        self.MINMAX_LAYOUT = widgets.QHBoxLayout()
        self.MINMAX_LAYOUT.setSpacing(0)
        self.DAY_LAYOUT = widgets.QHBoxLayout()
        self.CLOCK_LAYOUT = widgets.QGridLayout()
        self.SEARCH_LAYOUT = widgets.QHBoxLayout()

        self.LAYOUT.addLayout(self.HEADER_LAYOUT, 0, 0, 1, 0,
                              alignment=core.Qt.AlignmentFlag.AlignTop)

    def _setup_top_frames(self, main_window):
        self.left_frame = widgets.QFrame(self)
        self.left_frame.setMinimumHeight(int(main_window.width() / 5))
        self.left_frame.setMinimumWidth(int(main_window.width() / 5))
        self.left_frame.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Expanding,
        )
        self.left_frame.setStyleSheet("background-color: rgba(0, 0, 0, 50); border-radius: 10px;")
        self.left_frame.setLayout(self.LEFT_LAYOUT)
        self.LAYOUT.addWidget(self.left_frame, 1, 0)

        self.right_frame = widgets.QFrame(self)
        self.right_frame.setMinimumHeight(self.left_frame.height())
        self.right_frame.setMinimumWidth(self.left_frame.width())
        self.right_frame.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Expanding,
        )
        self.right_frame.setStyleSheet("background-color: rgba(0, 0, 0, 50); border-radius: 10px;")
        self.right_frame.setLayout(self.RIGHT_LAYOUT)
        self.LAYOUT.addWidget(self.right_frame, 1, 1)

        self.LEFT_LAYOUT.addLayout(self.TOP_LAYOUT)

    def _setup_left_content(self):
        container_geo = widgets.QFrame()
        container_geo.setFixedSize(1000, 50)
        container_geo.setStyleSheet(
            "background-color: None; border-radius: 0; padding-bottom: 5px;"
            "border-bottom: 2px solid rgba(255, 255, 255, 50);"
            "border-top: none; border-left: none; border-right: none;"
        )

        self.geo_icon = widgets.QLabel(container_geo)
        self.geo_icon.setGeometry(0, 2, container_geo.width(), container_geo.height())
        self.geo_icon.setStyleSheet("background-color: None;")
        self.geo_icon.setPixmap(QPixmap("media/Vector.png"))

        # текст задаётся в retranslateUi
        self.top_label = widgets.QLabel(container_geo)
        self.top_label.setGeometry(20, 0, container_geo.width(), container_geo.height())
        self.top_label.setStyleSheet(
            "border-radius: 0; font-size: 20px; font-weight: bold;"
            "background-color: None; padding-bottom: 5px;"
            "border-bottom: 0px; border-top: none; border-left: none;"
            "border-right: none; color: white;"
        )
        self.LEFT_LAYOUT.addWidget(container_geo, alignment=core.Qt.AlignmentFlag.AlignTop)

        self.city_label = widgets.QLabel(text=self.search.city)
        self.city_label.setStyleSheet(
            "font-size: 70px; font-weight: bold; background-color: None; color: white;"
        )
        self.LEFT_LAYOUT.addWidget(self.city_label, alignment=core.Qt.AlignmentFlag.AlignHCenter)
        self.LEFT_LAYOUT.addLayout(self.ICON_TEMP_LAYOUT)

        container_temp = widgets.QFrame()
        container_temp.setFixedSize(300, 150)
        container_temp.setStyleSheet("background-color: None")

        self.WEATHER_ICON = widgets.QLabel(container_temp)
        self.WEATHER_ICON.setFixedSize(100, 100)
        self.WEATHER_ICON.move(0, 20)
        self.WEATHER_ICON.setStyleSheet("background-color: None")

        self.temp_label = widgets.QLabel(container_temp)
        self.temp_label.setStyleSheet(
            "font-size: 100px; font-weight: bold; background-color: rgba(0, 0, 0, 0)"
        )
        self.temp_label.setGeometry(130, 0, container_temp.width(), container_temp.height())
        self.ICON_TEMP_LAYOUT.addWidget(container_temp)

        self.weather_label = widgets.QLabel()
        self.weather_label.setStyleSheet(
            "font-size: 40px; font-weight: bold; background-color: None"
        )
        self.LEFT_LAYOUT.addWidget(self.weather_label, alignment=core.Qt.AlignmentFlag.AlignHCenter)

        self.min_max_label = widgets.QLabel()
        self.min_max_label.setStyleSheet("font-size: 20px; background-color: rgba(0, 0, 0, 0)")
        self.MINMAX_LAYOUT.addWidget(self.min_max_label, alignment=core.Qt.AlignmentFlag.AlignHCenter)
        self.LEFT_LAYOUT.addLayout(self.MINMAX_LAYOUT)

    def _setup_right_content(self):
        container_today = widgets.QFrame()
        container_today.setFixedSize(1000, 50)
        container_today.setStyleSheet(
            "background-color: None; border-radius: 0; padding-bottom: 5px;"
            "border-bottom: 2px solid rgba(255, 255, 255, 50);"
            "border-top: none; border-left: none; border-right: none;"
        )
        # текст задаётся в retranslateUi
        self.TODAY_LABEL = widgets.QLabel(container_today)
        self.TODAY_LABEL.setGeometry(0, 0, container_today.width(), container_today.height())
        self.TODAY_LABEL.setStyleSheet(
            "border-radius: 0px; font-weight: bold; font-size: 20px;"
            "background-color: rgba(0, 0, 0, 0); border-bottom: 0px"
        )
        self.RIGHT_LAYOUT.addWidget(container_today, alignment=core.Qt.AlignmentFlag.AlignTop)
        self.RIGHT_LAYOUT.addLayout(self.DAY_LAYOUT)
        self.RIGHT_LAYOUT.addLayout(self.CLOCK_LAYOUT)

        now = datetime.datetime.now()
        # WEEK_DAY и DATE_LABEL — текст задаётся в retranslateUi
        self.WEEK_DAY = widgets.QLabel()
        self.WEEK_DAY.setStyleSheet(
            "font-size: 30px; font-weight: bold; background-color: rgba(0, 0, 0, 0)"
        )
        self.DATE_LABEL = widgets.QLabel(text=str(now.date()))
        self.DATE_LABEL.setStyleSheet(
            "font-size: 30px; font-weight: bold; background-color: rgba(0, 0, 0, 0)"
        )
        self.DAY_LAYOUT.addWidget(self.WEEK_DAY, alignment=core.Qt.AlignmentFlag.AlignTop)
        self.DAY_LAYOUT.addWidget(
            self.DATE_LABEL,
            alignment=core.Qt.AlignmentFlag.AlignRight | core.Qt.AlignmentFlag.AlignTop
        )

        container_clock = widgets.QFrame()
        container_clock.setFixedSize(200, 200)
        container_clock.setStyleSheet("background: none;")

        self.image_time = widgets.QLabel(container_clock)
        self.image_time.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.image_time.setPixmap(QPixmap("media/time.png"))
        self.image_time.setGeometry(0, 0, container_clock.width(), container_clock.height())
        self.image_time.setScaledContents(True)

        self.time_label = widgets.QLabel(container_clock)
        self.time_label.setStyleSheet(
            "font-size: 40px; font-weight: bold; background-color: rgba(0, 0, 0, 0)"
        )
        self.time_label.setGeometry(0, 0, container_clock.width(), container_clock.height())
        self.time_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.RIGHT_LAYOUT.addWidget(container_clock, alignment=core.Qt.AlignmentFlag.AlignCenter)

    def _setup_header(self):
        self.settings_button = widgets.QPushButton()
        self.settings_button.setFixedSize(50, 50)
        self.settings_button.setStyleSheet("background: rgba(0,0,0,50)")
        self.settings_button.setIcon(gui.QIcon("media/settings.png"))
        self.settings_button.clicked.connect(self.create_blur)
        self.HEADER_LAYOUT.addWidget(self.settings_button)

        # текст задаётся в retranslateUi
        self.settings_label = widgets.QLabel()
        self.settings_label.setStyleSheet(
            "font-size: 40px; font-weight: bold; background-color: rgba(0, 0, 0, 0)"
        )
        self.HEADER_LAYOUT.addWidget(self.settings_label)

    def _setup_search_widget(self):
        self.SEARCH_WIDGET = widgets.QFrame(self)
        self.SEARCH_WIDGET.setMinimumWidth(400)
        self.SEARCH_WIDGET.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Expanding,
        )
        self.SEARCH_WIDGET.setStyleSheet(
            "background-color: rgba(0, 0, 0, 60); border-radius: 10px; border: 2px ;"
        )
        self.SEARCH_WIDGET.setLayout(self.SEARCH_LAYOUT)

        self.SEARCH_IMAGE = widgets.QLabel(self.SEARCH_WIDGET)
        self.SEARCH_IMAGE.setPixmap(QPixmap("media/search_image.png"))
        self.SEARCH_IMAGE.setStyleSheet("background-color: None; border: 0px;")

        self.CROSS = widgets.QPushButton(self.SEARCH_WIDGET)
        self.CROSS.setFixedSize(20, 20)
        self.CROSS.setIcon(gui.QIcon("media/clear.png"))
        self.CROSS.setStyleSheet("background-color: None; border: 0px;")
        self.CROSS.clicked.connect(self.clear_text)

        self.search.setStyleSheet("border: 0px; background-color: rgba(0, 0, 0, 0)")

        self.SEARCH_LAYOUT.addWidget(self.SEARCH_IMAGE)
        self.SEARCH_LAYOUT.addWidget(self.search)
        self.SEARCH_LAYOUT.addWidget(self.CROSS)
        self.HEADER_LAYOUT.addWidget(self.SEARCH_WIDGET, alignment=core.Qt.AlignmentFlag.AlignRight)

        self.listwidget = Search_listwidget(self, search=self.search, width=self.SEARCH_WIDGET.width())
        self.listwidget.load_cities()
        self.listwidget.cities_funk()
        self.listwidget.setFixedHeight(200)
        self.listwidget.hide()
        self.search.textChanged.connect(self.listwidget_funk)

    def _setup_bottom_widgets(self):
        self.bottom1 = widgets.QFrame()
        self.bottom1.setMinimumHeight(100)
        self.bottom1.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Expanding,
        )
        self.bottom1.setStyleSheet("background-color: rgba(0,0,0,50); border-radius: 10px")

        bottom1_layout = widgets.QHBoxLayout()
        self.bottom1.setLayout(bottom1_layout)

        arrow_left = widgets.QPushButton()
        arrow_left.setIcon(gui.QIcon("media/arrows/arrow_left.png"))
        arrow_left.setFixedSize(50, 50)
        arrow_left.setStyleSheet("background: transparent; border: none;")
        arrow_left.pressed.connect(self.left_arrow_pressed)

        arrow_right = widgets.QPushButton()
        arrow_right.setIcon(gui.QIcon("media/arrows/arrow_right.png"))
        arrow_right.setFixedSize(50, 50)
        arrow_right.setStyleSheet("background: transparent; border: none;")
        arrow_right.pressed.connect(self.right_arrow_pressed)

        self.HOUR_FORECAST = Hour_forecast(parent=self.bottom1)
        bottom1_layout.addWidget(arrow_left)
        bottom1_layout.addWidget(self.HOUR_FORECAST)
        bottom1_layout.addWidget(arrow_right)
        self.LAYOUT.addWidget(self.bottom1, 2, 0, 1, 0)

        self.bottom2 = widgets.QFrame()
        self.bottom2.setStyleSheet("background-color: rgba(0,0,0,50); border-radius: 10px")
        self.bottom2.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Expanding,
        )
        bottom2_layout = widgets.QVBoxLayout()
        self.bottom2.setLayout(bottom2_layout)

        self.FORECAST12 = Forecast12(parent=self.bottom2)
        bottom2_layout.addWidget(self.FORECAST12)
        self.LAYOUT.addWidget(self.bottom2, 3, 0, 1, 2)

    # СОБЫТИЯ

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_listwidget_position()

    def update_listwidget_position(self):
        pos = self.SEARCH_WIDGET.mapTo(self, self.SEARCH_WIDGET.rect().bottomLeft())
        self.listwidget.move(pos.x(), pos.y() + 5)

    # ОБНОВЛЕНИЕ ДАННЫХ

    def update_data(self, data):
        self.data = data
        if not data or "list" not in data:
            return

        self.city_name = data["city"]["name"]
        self.temp = round(data["list"][0]["main"]["temp"])
        self.weather = data["list"][0]["weather"][0]["description"]
        self._min = data["list"][0]["main"]["temp_min"]
        self._max = data["list"][0]["main"]["temp_max"]
        self.icon = data["list"][0]["weather"][0]["icon"]

        self.city_label.setText(self.city_name)
        self.temp_label.setText(f"{self.temp}°")
        # weather — текст от API, не переводится
        self.weather_label.setText(self.weather)
        self.WEATHER_ICON.setPixmap(QPixmap(f"media/weather_icons/{self.icon}.png"))

        tz = datetime.timezone(datetime.timedelta(seconds=data["city"]["timezone"]))
        self.time_label.setText(datetime.datetime.now(tz).strftime("%H:%M"))

        self.HOUR_FORECAST.update_data(data=data)
        self.FORECAST12.update_data(data=data)

        # обновляем переводимую строку мин/макс
        self._update_minmax_label()

    def _update_minmax_label(self):
        """Собирает строку min/max с учётом текущего языка."""
        if self._min is not None and self._max is not None:
            self.min_max_label.setText(
                self.tr("min: %1°, max: %2°")
                    .replace("%1", str(round(self._min)))
                    .replace("%2", str(round(self._max)))
            )

    # ПОИСК

    def listwidget_funk(self):
        if self.search.text() == "":
            self.listwidget.hide()
        else:
            self.update_listwidget_position()
            self.listwidget.filter_cities(self.search.text())
            self.listwidget.raise_()
            self.listwidget.show()

    def clear_text(self):
        self.search.clear()

    # СТРЕЛКИ ПРОКРУТКИ

    def left_arrow_pressed(self):
        if not self.left_arrow_pressed_flag:
            self.HOUR_FORECAST.SCROLL_AREA.ensureVisible(0, 0)
            self.left_arrow_pressed_flag = True
            self.right_arrow_pressed_flag = False

    def right_arrow_pressed(self):
        if not self.right_arrow_pressed_flag:
            scrollbar = self.HOUR_FORECAST.SCROLL_AREA.horizontalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
            self.right_arrow_pressed_flag = True
            self.left_arrow_pressed_flag = False

    # НАСТРОЙКИ

    def create_blur(self):
        self.SETTINGS.show_window()
        blur = widgets.QGraphicsBlurEffect()
        blur.setBlurRadius(20)
        self.content_frame.setGraphicsEffect(blur)

    # ПЕРЕВОДЫ

    def retranslateUi(self):
        self.top_label.setText(self.tr("Current position"))
        self.TODAY_LABEL.setText(self.tr("Today"))
        self.settings_label.setText(self.tr("Settings"))

        # Дни недели — переводим текущий день
        days = [
            self.tr("Monday"),
            self.tr("Tuesday"),
            self.tr("Wednesday"),
            self.tr("Thursday"),
            self.tr("Friday"),
            self.tr("Saturday"),
            self.tr("Sunday"),
        ]
        self.WEEK_DAY.setText(days[datetime.datetime.now().weekday()])

        # Обновляем min/max если данные уже есть
        self._update_minmax_label()

        # Делегируем дочерним виджетам
        self.HOUR_FORECAST.retranslateUi()
        self.FORECAST12.retranslateUi()
        if hasattr(self.SETTINGS, 'retranslateUi'):
            self.SETTINGS.retranslateUi()

    def changeEvent(self, event):
        if event.type() == core.QEvent.Type.LanguageChange:
            self.retranslateUi()
        super().changeEvent(event)