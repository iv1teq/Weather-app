import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
import PyQt6.QtWebEngineWidgets as web_engine
import folium
import io
from config import MY_KEY
from .combo_box import Search_listwidget

class Settings(widgets.QFrame):
    def __init__(self, parent, content_frame, search, card_list, deleted_card_list):
        super().__init__(parent)
        self.card_list = card_list
        self.deleted_card_list = deleted_card_list
        self.search = search
        #window setup
        self.content_frame = content_frame
        self.setFixedSize(1000, 1000)
        self.setStyleSheet("background: #333333;")
        #layouts
        self.LAYOUT = widgets.QVBoxLayout()
        self.LAYOUT.setContentsMargins(20,20,20,20)
        self.LAYOUT.setSpacing(50)
        self.HEADER_LAYOUT = widgets.QHBoxLayout()
        # self.HEADER_LAYOUT.setSpacing(300)
        self.HEADER_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        # self.LEFT_LAYOUT = widgets.QVBoxLayout()
        # self.LEFT_LAYOUT.setSpacing(10)
        # self.LEFT_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        # self.LEFT_LAYOUT.setContentsMargins(0,0,15,0)
        self.RIGHT_LAYOUT = widgets.QGridLayout()
        self.RIGHT_LAYOUT.setColumnStretch(0, 1)
        self.RIGHT_LAYOUT.setColumnStretch(1, 1)

        self.BODY_LAYOUT = widgets.QHBoxLayout()
        self.BODY_LAYOUT.setSpacing(20)

        #left frame 
        self.LEFT_FRAME_LAYOUT = widgets.QVBoxLayout()
        self.LEFT_FRAME_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft )
        self.LEFT_FRAME_LAYOUT.setSpacing(8)
        self.LEFT_FRAME_LAYOUT.setContentsMargins(0,0,0,0)
        self.LEFT_FRAME = widgets.QFrame()
        self.LEFT_FRAME.setLayout(self.LEFT_FRAME_LAYOUT)
        self.LEFT_FRAME.setFixedSize(200,500)
        # self.LEFT_FRAME.setStyleSheet('background-color: white;')
        # self.LEFT_LAYOUT.addWidget(self.LEFT_FRAME, alignment = core.Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.LAYOUT)
        self.LAYOUT.addLayout(self.HEADER_LAYOUT)
        self.LAYOUT.addLayout(self.BODY_LAYOUT)
        self.BODY_LAYOUT.addWidget(self.LEFT_FRAME, alignment = core.Qt.AlignmentFlag.AlignTop)
        
        #bar
        bar = widgets.QFrame()
        bar.setFixedWidth(2)
        bar.setSizePolicy(widgets.QSizePolicy.Policy.Fixed, widgets.QSizePolicy.Policy.Expanding )
        bar.setStyleSheet('background-color: rgba(0,0,0,200)')
        self.BODY_LAYOUT.addWidget(bar)
        self.BODY_LAYOUT.addLayout(self.RIGHT_LAYOUT)

        
        # left buttons
        self.BUTTON_SEARCH_CITY = widgets.QPushButton( text = "Search city")
        
        self.BUTTON_APP_SIZE = widgets.QPushButton(text = "App size")

        self.BUTTON_LANGUAGE = widgets.QPushButton(text = "Language")

        self.BUTTON_LIST_IMAGE = widgets.QPushButton(text = "Image list")

        button_width = 200
        button_height = 60
        self.BUTTON_SEARCH_CITY.setFixedSize(button_width,button_height)
        self.BUTTON_APP_SIZE.setFixedSize(button_width,button_height)
        self.BUTTON_LANGUAGE.setFixedSize(button_width,button_height )
        self.BUTTON_LIST_IMAGE.setFixedSize(button_width,button_height)

        styleSheetButton = """
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
        
        self.BUTTON_APP_SIZE.setStyleSheet(styleSheetButton)
        self.BUTTON_LANGUAGE.setStyleSheet(styleSheetButton)
        self.BUTTON_LIST_IMAGE.setStyleSheet(styleSheetButton)
        self.BUTTON_SEARCH_CITY.setStyleSheet(styleSheetButton)
        

        
        self.LEFT_FRAME_LAYOUT.addWidget(self.BUTTON_SEARCH_CITY)
        self.LEFT_FRAME_LAYOUT.addWidget(self.BUTTON_APP_SIZE)
        self.LEFT_FRAME_LAYOUT.addWidget(self.BUTTON_LANGUAGE)
        self.LEFT_FRAME_LAYOUT.addWidget(self.BUTTON_LIST_IMAGE)
        
        
        # font-size: 30px hover  background-color: rgba(0, 0, 0, 30)
        




        #header label

        label_settings = widgets.QLabel(text = 'Settings')
        label_settings.setStyleSheet('font-size: 45px; font-weight: bold;')
        self.HEADER_LAYOUT.addWidget(label_settings)

        #close button

        close_button = widgets.QPushButton()
        close_button.setFixedSize(100,100)
        close_icon = gui.QIcon('media/x.png')
        close_button.setIcon(close_icon)
        self.HEADER_LAYOUT.addWidget(close_button)
        close_button.clicked.connect(self.hide_window)

        #right area title

        right_label = widgets.QLabel(text = 'Find a city')
        self.SEARCH_LAYOUT = widgets.QVBoxLayout()
        self.RIGHT_LAYOUT.addLayout(self.SEARCH_LAYOUT, 1, 0, alignment=core.Qt.AlignmentFlag.AlignTop)
        right_label.setStyleSheet("font-size: 35px")
        self.RIGHT_LAYOUT.addWidget(right_label, 0,0, alignment = core.Qt.AlignmentFlag.AlignTop)

        #mini map

        map = folium.Map(
            location=(50, 50),
            zoom_start=13,
            tiles=f"https://tiles.stadiamaps.com/tiles/osm_bright/{{z}}/{{x}}/{{y}}{{r}}.png?api_key={MY_KEY}",
            attr="Stadia Maps",
            zoom_control=False,
            attributionControl=False
        )
        webView = web_engine.QWebEngineView()
        webView.setFixedSize(core.QSize(400,400))
        
        data = io.BytesIO()
        map.save(data, close_file = False)
        get_data = data.getvalue()
        webView.setHtml(get_data.decode())

        self.RIGHT_LAYOUT.addWidget(webView, 1, 1, alignment=core.Qt.AlignmentFlag.AlignTop)
        
        self.country_label = widgets.QLabel(text = "Country")
        self.city_label = widgets.QLabel(text = "City")
        self.coordinates_label = widgets.QLabel(text = "Coordinates")
        self.COUNTRY_SEARCH = widgets.QLineEdit()

        self.CITY_SEARCH = widgets.QLineEdit()
        

        self.COORDINATES_SEARCH = widgets.QLineEdit()
        self.SAVE_BUTTON = widgets.QPushButton(text="Save")
        self.SAVE_BUTTON.setStyleSheet("background-color: #383838; color: white")
        self.country_label.setStyleSheet("font-size: 20px")
        self.city_label.setStyleSheet("font-size: 20px")
        self.coordinates_label.setStyleSheet("font-size: 20px")
        self.COUNTRY_SEARCH.setStyleSheet("background-color: white")
        self.CITY_SEARCH.setStyleSheet("background-color: white")
        self.COORDINATES_SEARCH.setStyleSheet("background-color: white")
        self.SAVE_BUTTON.setFixedSize(80, 50)
        self.COORDINATES_SEARCH.setFixedSize(200, 50)
        self.COUNTRY_SEARCH.setFixedSize(200, 50)
        self.CITY_SEARCH.setFixedSize(200, 50)
        
        
        self.SEARCH_LAYOUT.addWidget(self.country_label)
        self.SEARCH_LAYOUT.addWidget(self.COUNTRY_SEARCH)
        self.SEARCH_LAYOUT.addWidget(self.city_label)
        self.SEARCH_LAYOUT.addWidget(self.CITY_SEARCH)
        self.SEARCH_LAYOUT.addWidget(self.coordinates_label)
        self.SEARCH_LAYOUT.addWidget(self.COORDINATES_SEARCH)
        self.SEARCH_LAYOUT.addWidget(self.SAVE_BUTTON)
        
        #layout for added citys

        self.LABEL_ADDED_CITIES_LAYOUT = widgets.QVBoxLayout()
        #container for layout

        self.CITY_ADDED_FRAME = widgets.QFrame()
        self.CITY_ADDED_FRAME.setFixedWidth(600)
        self.CITY_ADDED_FRAME.setLayout(self.LABEL_ADDED_CITIES_LAYOUT)

        self.RIGHT_LAYOUT.addWidget(self.CITY_ADDED_FRAME, 2, 0, 1, 2)
        
        #list widget + search

        self.country_listwidget = Search_listwidget(self, search = self.COUNTRY_SEARCH, width = 200 )
        self.country_listwidget.countries_funk()
        self.country_listwidget.setFixedHeight(200)
        self.country_listwidget.hide()
        self.COUNTRY_SEARCH.textChanged.connect(self.country_listwidget_funk)
        
        self.city_listwidget = Search_listwidget(self, search = self.CITY_SEARCH, width = 200 )
        self.city_listwidget.cities_funk()
        self.city_listwidget.setFixedHeight(200)
        self.city_listwidget.hide()
        self.CITY_SEARCH.textChanged.connect(self.city_listwidget_funk)

        self.country_listwidget.country_selected.connect(
    self.city_listwidget.load_cities_by_country
)
        self.create_cards()
        
        
    def update_country_listwidget_position(self):
        pos = self.COUNTRY_SEARCH.mapTo(self, self.COUNTRY_SEARCH.rect().bottomLeft())
        self.country_listwidget.move(pos.x(), pos.y() + 5)

    def update_city_listwidget_position(self):
        pos = self.CITY_SEARCH.mapTo(self, self.CITY_SEARCH.rect().bottomLeft())
        self.city_listwidget.move(pos.x(), pos.y() + 5)


    def hide_window(self):
        self.hide()
        self.content_frame.setGraphicsEffect(None)
    
    def show_window(self):  # добавь этот метод
        self.create_cards()  # обновляем список при открытии
        self.show()


    def country_listwidget_funk(self):
        if self.COUNTRY_SEARCH.text() == "":
                self.country_listwidget.hide()
        else:
                self.update_country_listwidget_position()
                self.country_listwidget.filter_countries(self.COUNTRY_SEARCH.text())
                self.country_listwidget.raise_()
                self.country_listwidget.show()
                
    def city_listwidget_funk(self):
        if self.CITY_SEARCH.text() == "":
                self.city_listwidget.hide()
        else:
                self.update_city_listwidget_position()
                self.city_listwidget.filter_cities(self.CITY_SEARCH.text())
                self.city_listwidget.raise_()
                self.city_listwidget.show()
                

    def create_cards(self):
        # очищаем предыдущие карточки
        for i in reversed(range(self.LABEL_ADDED_CITIES_LAYOUT.count())):
            item = self.LABEL_ADDED_CITIES_LAYOUT.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()

        for city in self.card_list:
            city_widget = widgets.QFrame()
            city_layout = widgets.QHBoxLayout()
            city_widget.setLayout(city_layout)

            city_label = widgets.QLabel(text=city)
            city_label.setStyleSheet('font-size: 15px; color: white;')

            delete_button = widgets.QPushButton()
            delete_icon = gui.QIcon('media/delete_button.png')
            delete_button.setIcon(delete_icon)
            delete_button.clicked.connect(lambda checked, c=city: self.delete_cards(c))

            city_layout.addWidget(city_label)
            city_layout.addWidget(delete_button)

            self.LABEL_ADDED_CITIES_LAYOUT.addWidget(city_widget)  # ← добавляем в layout!
    def delete_cards(self, city_name):
        self.card_list.remove(city_name)
        self.deleted_card_list.append(city_name)
        self.create_cards()  # просто перерисовываем список
        
    def update(self):
        # self.delete_cards()
        self.create_cards()
        print("+")

