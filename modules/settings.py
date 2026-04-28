import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
import PyQt6.QtWebEngineWidgets as web_engine
import folium
import io
from config import MY_KEY
from .combo_box import Search_listwidget
from .search import Search
from utils import api_request


class Settings(widgets.QFrame):
    def __init__(self, parent, content_frame, search, card_list, deleted_card_list,
                 left_area, window_height, window_width):
        super().__init__(parent)
        self.setAttribute(core.Qt.WidgetAttribute.WA_StyledBackground, True)

        self.main_window = self.window()
        self.card_list = card_list
        self.deleted_card_list = deleted_card_list
        self.search = search
        self.left_area = left_area
        self.content_frame = content_frame
        self.window_height = window_height
        self.window_width = window_width
        self.last_lat = 50
        self.last_lon = 50

        # QTranslator хранится здесь, чтобы не удалился сборщиком мусора
        self._translator = core.QTranslator()
        self._current_lang = 'en'

        self._setup_window()
        self._setup_size_panel()
        self._setup_language_panel()
        self._setup_layouts()
        self._setup_left_panel()
        self._setup_header()
        self._setup_right_panel()
        self._setup_search_fields()
        self._setup_city_list()
        self._setup_listwidgets()

        self.create_cards()

        self.BUTTON_SEARCH_CITY.clicked.connect(self.open_search_city)
        self.BUTTON_APP_SIZE.clicked.connect(self.open_app_size)
        self.BUTTON_LANGUAGE.clicked.connect(self.open_app_language)

        self.retranslateUi()

    # ИНИЦИАЛИЗАЦИЯ

    def _setup_window(self):
        self.resize(1000, 1000)
        self.setStyleSheet('background-color: transparent;')
        self.search_city_container = widgets.QWidget()
        self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.container = widgets.QFrame(self)
        self.container.setGeometry(self.rect())
        self.container.setStyleSheet("""
            QFrame#container {
                background-color: rgba(0, 0, 0, 190);
                border-radius: 16px;
            }
            QLabel { background-color: transparent; }
            QPushButton { background-color: transparent; }
            QRadioButton { background-color: transparent; }
            QFrame { background-color: transparent; }
            QWidget { background-color: transparent; }
        """)
        self.container.setObjectName("container")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.container.setGeometry(self.rect())

    def _setup_size_panel(self):
        self.size_container = widgets.QWidget(
            self.container if hasattr(self, 'container') else None
        )
        self.size_layout = widgets.QVBoxLayout()
        self.size_container.setLayout(self.size_layout)
        self.size_container.hide()

        # текст задаётся в retranslateUi
        self.size_label = widgets.QLabel()
        self.size_layout.addWidget(self.size_label)

        self.radio_group = widgets.QButtonGroup()
        buttons = [
            ("1200x800",  1200, 800),
            ("1440x1024", 1440, 1024),
            ("1512x982",  1512, 982),
            ("1728x1117", 1728, 1117),
        ]
        for label, w, h in buttons:
            btn = widgets.QRadioButton(parent=self.size_container, text=label)
            self.radio_group.addButton(btn)
            self.size_layout.addWidget(btn)
            btn.clicked.connect(lambda checked, w=w, h=h: self.set_size(w, h))

    def _setup_language_panel(self):
        self.language_container = widgets.QWidget()
        self.language_layout = widgets.QVBoxLayout()
        self.language_container.setLayout(self.language_layout)
        self.language_container.hide()

        # текст задаётся в retranslateUi
        self.choose_language_label = widgets.QLabel()
        self.language_label = widgets.QLabel()

        self.box_language = widgets.QComboBox()
        # индексы фиксированы: 0 = Ukrainian, 1 = English
        self.box_language.addItem('Ukrainian')
        self.box_language.addItem('English')
        self.box_language.currentIndexChanged.connect(self._on_language_changed)

        self.language_layout.addWidget(self.choose_language_label)
        self.language_layout.addWidget(self.language_label)
        self.language_layout.addWidget(self.box_language)

    def _setup_layouts(self):
        self.LAYOUT = widgets.QVBoxLayout()
        self.LAYOUT.setContentsMargins(20, 20, 20, 20)
        self.LAYOUT.setSpacing(50)

        self.HEADER_LAYOUT = widgets.QHBoxLayout()
        self.HEADER_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        self.BODY_LAYOUT = widgets.QHBoxLayout()
        self.BODY_LAYOUT.setSpacing(20)
        self.BODY_LAYOUT.setStretch(0, 1)
        self.BODY_LAYOUT.setStretch(1, 0)
        self.BODY_LAYOUT.setStretch(2, 4)

        self.RIGHT_LAYOUT = widgets.QGridLayout()
        self.RIGHT_LAYOUT.setColumnStretch(0, 1)
        self.RIGHT_LAYOUT.setColumnStretch(1, 1)
        self.RIGHT_LAYOUT.addWidget(self.size_container, 1, 0)
        self.RIGHT_LAYOUT.addWidget(self.language_container, 1, 0)

        self.container.setLayout(self.LAYOUT)
        self.LAYOUT.addLayout(self.HEADER_LAYOUT)
        self.LAYOUT.addLayout(self.BODY_LAYOUT)

    def _setup_left_panel(self):
        self.LEFT_FRAME_LAYOUT = widgets.QVBoxLayout()
        self.LEFT_FRAME_LAYOUT.setAlignment(
            core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft
        )
        self.LEFT_FRAME_LAYOUT.setSpacing(8)
        self.LEFT_FRAME_LAYOUT.setContentsMargins(0, 0, 0, 0)

        self.LEFT_FRAME = widgets.QFrame()
        self.LEFT_FRAME.setLayout(self.LEFT_FRAME_LAYOUT)
        self.LEFT_FRAME.setMinimumWidth(150)
        self.BODY_LAYOUT.addWidget(self.LEFT_FRAME, alignment=core.Qt.AlignmentFlag.AlignTop)

        bar = widgets.QFrame()
        bar.setFixedWidth(2)
        bar.setSizePolicy(widgets.QSizePolicy.Policy.Fixed, widgets.QSizePolicy.Policy.Expanding)
        bar.setStyleSheet("background-color: rgba(100,0,0,200);")
        self.BODY_LAYOUT.addWidget(bar)
        self.BODY_LAYOUT.addLayout(self.RIGHT_LAYOUT)

        btn_style = """
            QPushButton {
                background-color: transparent;
                border-radius: 8px;
                font-size: 25px;
                color: white;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 30);
            }
        """
        # текст кнопок задаётся в retranslateUi
        nav_buttons = [
            ("BUTTON_SEARCH_CITY",),
            ("BUTTON_APP_SIZE",),
            ("BUTTON_LANGUAGE",),
            ("BUTTON_LIST_IMAGE",),
        ]
        for (attr,) in nav_buttons:
            btn = widgets.QPushButton()
            btn.setMinimumHeight(50)
            btn.setStyleSheet(btn_style)
            setattr(self, attr, btn)
            self.LEFT_FRAME_LAYOUT.addWidget(btn)

    def _setup_header(self):
        # текст задаётся в retranslateUi
        self.header_title = widgets.QLabel()
        self.header_title.setStyleSheet("font-size: 45px; font-weight: bold; color: white;")
        self.HEADER_LAYOUT.addWidget(self.header_title)

        close_btn = widgets.QPushButton()
        close_btn.setFixedSize(100, 100)
        close_btn.setIcon(gui.QIcon("media/x.png"))
        close_btn.clicked.connect(self.hide_window)
        self.HEADER_LAYOUT.addWidget(close_btn)

    def _setup_right_panel(self):
        # текст задаётся в retranslateUi
        self.right_label = widgets.QLabel()
        self.right_label.setStyleSheet("font-size: 35px; color: white;")
        self.RIGHT_LAYOUT.addWidget(
            self.right_label, 0, 0, alignment=core.Qt.AlignmentFlag.AlignTop
        )

        self.SEARCH_LAYOUT = widgets.QVBoxLayout()
        self.RIGHT_LAYOUT.addLayout(
            self.SEARCH_LAYOUT, 1, 0, alignment=core.Qt.AlignmentFlag.AlignTop
        )

        initial_map = folium.Map(
            location=(self.last_lat, self.last_lon),
            zoom_start=13,
            tiles=(
                f"https://tiles.stadiamaps.com/tiles/osm_bright/{{z}}/{{x}}/{{y}}{{r}}.png"
                f"?api_key={MY_KEY}"
            ),
            attr="Stadia Maps",
            zoom_control=False,
            attributionControl=False,
        )
        self.webView = web_engine.QWebEngineView()
        self.webView.setMinimumSize(200, 200)
        self.webView.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Expanding,
        )
        buf = io.BytesIO()
        initial_map.save(buf, close_file=False)
        self.webView.setHtml(buf.getvalue().decode())
        self.RIGHT_LAYOUT.addWidget(
            self.webView, 1, 1, alignment=core.Qt.AlignmentFlag.AlignTop
        )

    def _setup_search_fields(self):
        label_style = "font-size: 20px; color: white;"
        field_style = "background-color: white; color: black;"

        # текст задаётся в retranslateUi
        self.country_label = widgets.QLabel()
        self.city_label_widget = widgets.QLabel()       # переименовано: не конфликтует с city_label из RightArea
        self.coordinates_label = widgets.QLabel()

        self.country_label.setStyleSheet(label_style)
        self.city_label_widget.setStyleSheet(label_style)
        self.coordinates_label.setStyleSheet(label_style)

        self.COUNTRY_SEARCH = Search(self.container)
        self.COUNTRY_SEARCH.setStyleSheet(field_style)
        self.COUNTRY_SEARCH.setMinimumHeight(40)
        self.COUNTRY_SEARCH.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Fixed,
        )

        self.CITY_SEARCH = Search(self.container)
        self.CITY_SEARCH.setStyleSheet(field_style)
        self.CITY_SEARCH.setMinimumHeight(40)
        self.CITY_SEARCH.setEnabled(False)

        self.COORDINATES_SEARCH = widgets.QLabel()
        self.COORDINATES_SEARCH.setStyleSheet(field_style)
        self.COORDINATES_SEARCH.setMinimumHeight(40)

        # текст задаётся в retranslateUi
        self.SAVE_BUTTON = widgets.QPushButton()
        self.SAVE_BUTTON.setFixedSize(80, 50)
        self.SAVE_BUTTON.setStyleSheet("background-color: rgba(0, 0, 0, 190); color: white;")
        self.SAVE_BUTTON.clicked.connect(self.save_city)

        for w in [
            self.country_label, self.COUNTRY_SEARCH,
            self.city_label_widget, self.CITY_SEARCH,
            self.coordinates_label, self.COORDINATES_SEARCH,
            self.SAVE_BUTTON,
        ]:
            self.SEARCH_LAYOUT.addWidget(w)

    def _setup_city_list(self):
        self.LABEL_ADDED_CITIES_LAYOUT = widgets.QVBoxLayout()
        self.CITY_ADDED_FRAME = widgets.QFrame()
        self.CITY_ADDED_FRAME.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Preferred,
        )
        self.CITY_ADDED_FRAME.setLayout(self.LABEL_ADDED_CITIES_LAYOUT)
        self.RIGHT_LAYOUT.addWidget(self.CITY_ADDED_FRAME, 2, 0, 1, 2)

    def _setup_listwidgets(self):
        self.country_listwidget = Search_listwidget(
            self.container, search=self.COUNTRY_SEARCH, width=200
        )
        self.country_listwidget.countries_funk()
        self.country_listwidget.setFixedHeight(200)
        self.country_listwidget.hide()
        self.COUNTRY_SEARCH.textChanged.connect(self.country_listwidget_funk)

        self.city_listwidget = Search_listwidget(
            self.container, search=self.CITY_SEARCH, width=200
        )
        self.city_listwidget.cities_funk()
        self.city_listwidget.setFixedHeight(200)
        self.city_listwidget.hide()
        self.CITY_SEARCH.textChanged.connect(self.city_listwidget_funk)

        self.country_listwidget.country_selected.connect(
            self.city_listwidget.load_cities_by_country
        )
        self.country_listwidget.country_selected.connect(self.on_country_selected)

    # ПОЗИЦИОНИРОВАНИЕ ВЫПАДАЮЩИХ СПИСКОВ

    def update_country_listwidget_position(self):
        pos = self.COUNTRY_SEARCH.mapTo(
            self.container, self.COUNTRY_SEARCH.rect().bottomLeft()
        )
        self.country_listwidget.move(pos.x(), pos.y() + 5)

    def update_city_listwidget_position(self):
        pos = self.CITY_SEARCH.mapTo(
            self.container, self.CITY_SEARCH.rect().bottomLeft()
        )
        self.city_listwidget.move(pos.x(), pos.y() + 5)

    # ОБРАБОТКА ВВОДА

    def country_listwidget_funk(self):
        text = self.COUNTRY_SEARCH.text()
        if text == "":
            self.country_listwidget.hide()
            self.CITY_SEARCH.clear()
            self.CITY_SEARCH.setEnabled(False)
            self.city_listwidget.cities = []
            self.city_listwidget.hide()
        else:
            self.city_listwidget.hide()
            self.update_country_listwidget_position()
            self.country_listwidget.filter_countries(text)
            self.country_listwidget.raise_()
            self.country_listwidget.show()

    def city_listwidget_funk(self):
        if not self.city_listwidget.cities:
            self.city_listwidget.hide()
            return
        text = self.CITY_SEARCH.text()
        self.country_listwidget.hide()
        if text == "":
            self.city_listwidget.hide()
        else:
            self.update_city_listwidget_position()
            self.city_listwidget.filter_cities(text)
            self.city_listwidget.raise_()
            self.city_listwidget.show()

    def on_country_selected(self, country_name):
        self.CITY_SEARCH.setEnabled(True)
        self.CITY_SEARCH.clear()
        self.CITY_SEARCH.setFocus()

    # КАРТОЧКИ ГОРОДОВ

    def create_cards(self):
        for i in reversed(range(self.LABEL_ADDED_CITIES_LAYOUT.count())):
            item = self.LABEL_ADDED_CITIES_LAYOUT.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()

        for city in self.card_list:
            self.city_widget = widgets.QFrame()
            city_layout = widgets.QHBoxLayout()
            self.city_widget.setLayout(city_layout)

            city_label = widgets.QLabel(text=city)
            city_label.setStyleSheet("font-size: 15px; color: white;")

            delete_btn = widgets.QPushButton()
            delete_btn.setIcon(gui.QIcon("media/delete_button.png"))
            delete_btn.clicked.connect(lambda checked, c=city: self.delete_cards(c))

            city_layout.addWidget(city_label)
            city_layout.addWidget(delete_btn)
            self.LABEL_ADDED_CITIES_LAYOUT.addWidget(self.city_widget)

    def delete_cards(self, city_name):
        if city_name in self.card_list:
            self.card_list.remove(city_name)
        self.left_area.remove_card_by_name(city_name)
        self.create_cards()

    def save_city(self):
        city = self.CITY_SEARCH.text().strip()
        if not city or city in self.card_list:
            return

        self.left_area.search.city = city
        data = api_request(city)

        if data and "list" in data:
            self.left_area.update_data(data)
            self.CITY_SEARCH.clearFocus()
            self.COUNTRY_SEARCH.clearFocus()
            self.create_cards()

            lat = data["city"]["coord"]["lat"]
            lon = data["city"]["coord"]["lon"]
            self.update_map(lat, lon)

            new_card = self.left_area.scroll_layout.itemAt(0)
            if new_card and new_card.widget():
                self.left_area.change_card_bg(new_card.widget())
        else:
            print(f"Город не найден: {city}")

    # КАРТА

    def update_map(self, lat, lon):
        self.last_lat = lat
        self.last_lon = lon

        new_map = folium.Map(
            location=(lat, lon),
            zoom_start=13,
            tiles=(
                f"https://tiles.stadiamaps.com/tiles/osm_bright/{{z}}/{{x}}/{{y}}{{r}}.png"
                f"?api_key={MY_KEY}"
            ),
            attr="Stadia Maps",
            zoom_control=False,
            attributionControl=False,
        )
        folium.Marker(location=(lat, lon)).add_to(new_map)

        buf = io.BytesIO()
        new_map.save(buf, close_file=False)
        self.webView.setHtml(buf.getvalue().decode())

    # ПОКАЗ / СКРЫТИЕ

    def show_window(self):
        self.create_cards()
        self.update_geometry()
        active = self.left_area.active_card
        if active and active.data and "city" in active.data:
            lat = active.data["city"]["coord"]["lat"]
            lon = active.data["city"]["coord"]["lon"]
            self.update_map(lat, lon)
        self.show()

    def hide_window(self):
        self.hide()
        self.content_frame.setGraphicsEffect(None)

    def open_search_city(self):
        self.size_container.hide()
        self.language_container.hide()
        self.SEARCH_LAYOUT.setEnabled(True)
        for i in range(self.SEARCH_LAYOUT.count()):
            item = self.SEARCH_LAYOUT.itemAt(i)
            if item.widget():
                item.widget().show()
        self.webView.show()
        self.right_label.setText(self.tr("Find a city"))

    def open_app_size(self):
        for i in range(self.SEARCH_LAYOUT.count()):
            item = self.SEARCH_LAYOUT.itemAt(i)
            if item.widget():
                item.widget().hide()
        self.size_container.show()
        self.language_container.hide()
        self.webView.hide()
        self.right_label.setText(self.tr("Choose app size"))

    def open_app_language(self):
        for i in range(self.SEARCH_LAYOUT.count()):
            item = self.SEARCH_LAYOUT.itemAt(i)
            if item.widget():
                item.widget().hide()
        self.size_container.hide()
        self.language_container.show()
        self.webView.hide()
        self.right_label.setText(self.tr("Choose a language"))

    def set_size(self, width, height):
        self.window_width = width
        self.window_height = height
        self.window().resize(width, height)
        self.setFixedSize(int(width / 2), int(height / 1.5))

    def update_geometry(self):
        parent = self.parent()
        if not parent:
            return
        w = parent.width()
        h = parent.height()
        new_w = int(w / 2)
        new_h = int(h * 2 / 3)
        x = (w - new_w) // 2
        y = (h - new_h) // 2
        self.setGeometry(x, y, new_w, new_h)

    # СМЕНА ЯЗЫКА

    def _on_language_changed(self, index):
        """Вызывается при выборе языка в QComboBox."""
        app = core.QCoreApplication.instance()

        # снимаем старый переводчик
        app.removeTranslator(self._translator)

        if index == 0:
            # Ukrainian
            loaded = self._translator.load("translations/uk.qm")
            self._current_lang = 'uk'
        else:
            # English — пустой переводчик (исходные строки)
            loaded = False
            self._current_lang = 'en'

        if loaded:
            app.installTranslator(self._translator)
        # LanguageChange event рассылается автоматически всем виджетам

    # ПЕРЕВОДЫ

    def retranslateUi(self):
        self.header_title.setText(self.tr("Settings"))
        self.right_label.setText(self.tr("Find a city"))

        # Кнопки левой панели
        self.BUTTON_SEARCH_CITY.setText(self.tr("Search city"))
        self.BUTTON_APP_SIZE.setText(self.tr("App size"))
        self.BUTTON_LANGUAGE.setText(self.tr("Language"))
        self.BUTTON_LIST_IMAGE.setText(self.tr("Image list"))

        # Панель размера
        self.size_label.setText(self.tr("Choose app size"))

        # Панель языка
        self.choose_language_label.setText(self.tr("Choose the language"))
        self.language_label.setText(self.tr("Language"))

        # Поля поиска города
        self.country_label.setText(self.tr("Country"))
        self.city_label_widget.setText(self.tr("City"))
        self.coordinates_label.setText(self.tr("Coordinates"))
        self.SAVE_BUTTON.setText(self.tr("Save"))

    def changeEvent(self, event):
        if event.type() == core.QEvent.Type.LanguageChange:
            self.retranslateUi()
        super().changeEvent(event)