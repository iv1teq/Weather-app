import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui




class Settings(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent )
        #window setup
        self.setFixedSize(1000, 1000)
        self.setStyleSheet("background: #333333;")
        #layouts
        self.LAYOUT = widgets.QVBoxLayout()
        self.LAYOUT.setContentsMargins(40,40,40,40)
        self.LAYOUT.setSpacing(50)
        self.HEADER_LAYOUT = widgets.QHBoxLayout()
        # self.HEADER_LAYOUT.setSpacing(300)
        self.HEADER_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.LEFT_LAYOUT = widgets.QVBoxLayout()
        self.LEFT_LAYOUT.setSpacing(10)
        self.LEFT_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.RIGHT_LAYOUT = widgets.QGridLayout()
        self.BODY_LAYOUT = widgets.QHBoxLayout()
        
        self.setLayout(self.LAYOUT)
        self.LAYOUT.addLayout(self.HEADER_LAYOUT)
        self.LAYOUT.addLayout(self.BODY_LAYOUT)
        self.BODY_LAYOUT.addLayout(self.LEFT_LAYOUT)
        
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
        
        self.BUTTON_SEARCH_CITY.setFixedSize(200, 70)
        self.BUTTON_APP_SIZE.setFixedSize(200,70)
        self.BUTTON_LANGUAGE.setFixedSize(200,70)
        self.BUTTON_LIST_IMAGE.setFixedSize(200,70)

        styleSheetButton = """
    QPushButton {
        background-color: transparent;
        border-radius: 12px;
        font-size: 30px;
    }
    QPushButton:hover {
        background-color: rgba(0, 0, 0, 30);
    }
    """
        
        self.BUTTON_APP_SIZE.setStyleSheet(styleSheetButton)
        self.BUTTON_LANGUAGE.setStyleSheet(styleSheetButton)
        self.BUTTON_LIST_IMAGE.setStyleSheet(styleSheetButton)
        self.BUTTON_SEARCH_CITY.setStyleSheet(styleSheetButton)
        

        
        self.LEFT_LAYOUT.addWidget(self.BUTTON_SEARCH_CITY)
        self.LEFT_LAYOUT.addWidget(self.BUTTON_APP_SIZE)
        self.LEFT_LAYOUT.addWidget(self.BUTTON_LANGUAGE)
        self.LEFT_LAYOUT.addWidget(self.BUTTON_LIST_IMAGE)
        
        
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
        close_button.clicked.connect(self.hide)
        #right area title
        right_label = widgets.QLabel(text = 'Find a city')
        
        right_label.setStyleSheet("font-size: 35px")
        self.RIGHT_LAYOUT.addWidget(right_label, 0,0, alignment = core.Qt.AlignmentFlag.AlignTop)
    def hide_window(self):
        self.hide()