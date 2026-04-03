import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
import PyQt6.QtWebEngineWidgets as web_engine
import folium
import io



class Settings(widgets.QFrame):
    def __init__(self, parent, content_frame):
        super().__init__(parent )
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
        MY_KEY = "11dc5041-69ae-4e1e-88a4-cfd35a913235"

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
        
        #layout for one city
        self.CITY_LAYOUT = widgets.QHBoxLayout()
        #city 
        #city container
        self.CITY_WIDGET = widgets.QFrame()

        self.CITY_LABEL = widgets.QLabel(text = 'Dnepr') #here citys info from search
        self.CITY_LABEL.setStyleSheet('font-size: 15px;')
        self.CITY_WIDGET.setLayout(self.CITY_LAYOUT)
        #del button
        self.DELETE_BUTTON = widgets.QPushButton()
        self.DELETE_ICON = gui.QIcon('media/delete_button.png')
        self.DELETE_BUTTON.setIcon(self.DELETE_ICON)
        #adding city to the main citys layout 
        self.CITY_LAYOUT.addWidget(self.CITY_LABEL)
        self.CITY_LAYOUT.addWidget(self.DELETE_BUTTON)# use this for added citys in main app and in settings
        
        # add city label to the container layout
        self.LABEL_ADDED_CITIES_LAYOUT.addWidget(self.CITY_WIDGET)
        # add container to the layout
        self.RIGHT_LAYOUT.addWidget(self.CITY_ADDED_FRAME, 2, 0, 1, 2)
        
        
        
        
        
        

    def hide_window(self):
        self.hide()
        self.content_frame.setGraphicsEffect(None)
    
    
    