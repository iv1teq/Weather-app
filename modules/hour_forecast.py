import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
from PyQt6.QtGui import QPixmap

class Hour_forecast(widgets.QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        data = None
        self.LAYOUT = widgets.QVBoxLayout()
        self.setLayout(self.LAYOUT)
        self.WEATHER_LABEL = widgets.QLabel(self, text = "какая-то погода до конца дня")
        self.WEATHER_LABEL.setStyleSheet("font-size: 20px")
        self.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding )
        self.LAYOUT.addWidget(self.WEATHER_LABEL, alignment=core.Qt.AlignmentFlag.AlignTop)
        
        self.SCROLL_AREA = widgets.QScrollArea(self)
        self.SCROLL_AREA.setWidgetResizable(True)
        self.SCROLL_AREA.setStyleSheet("border: none;")
        self.SCROLL_AREA.setStyleSheet("""
    background-color: transparent;  
    border: none;                   
""")
        # self.SCROLL_AREA.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.SCROLL_AREA.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SCROLL_FRAME = widgets.QFrame()
        self.SCROLL_LAYOUT = widgets.QHBoxLayout(self.SCROLL_FRAME)
        # self.SCROLL_FRAME.minimumWidth(500)
        # self.SCROLL_FRAME.minimumHeight(200)
        self.SCROLL_FRAME.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding)
        # self.SCROLL_LAYOUT.setContentsMargins(5,5,5,5)
        # self.SCROLL_LAYOUT.setSpacing(10)
        
        
        self.SCROLL_AREA.setWidget(self.SCROLL_FRAME)
        self.LAYOUT.addWidget(self.SCROLL_AREA)
            

        self.setStyleSheet('background-color: None')
    def update_data(self, data):
        if not data or "list" not in data:
            return
        temp_list = []
        weather_list = []
        
        for i in range(0, 9):
            for _ in range(3):
                temp_list.append(data["list"][i]["main"]["temp"])
                weather_list.append(data["list"][i]["weather"][0]["main"])
            
            
            
        for hour in range(24):
            self.FRAME_LAYOUT = widgets.QVBoxLayout()
            self.FRAME = widgets.QFrame(self.SCROLL_FRAME)
            self.FRAME.setLayout(self.FRAME_LAYOUT)
            self.TIME_LABEL = widgets.QLabel(text = str(hour))
            self.IMAGE_LABEL = widgets.QLabel()
            weather_pixmap = QPixmap(f"media/hour_forecast_icons/{weather_list[hour]}.png")
            print()
            self.IMAGE_LABEL.setPixmap(weather_pixmap)
            self.TEMP_LABEL = widgets.QLabel(self.SCROLL_FRAME, text = str(round(temp_list[hour])))
            self.FRAME_LAYOUT.addWidget(self.TIME_LABEL)
            self.FRAME_LAYOUT.addWidget(self.IMAGE_LABEL)
            self.FRAME_LAYOUT.addWidget(self.TEMP_LABEL)
            self.SCROLL_LAYOUT.addWidget(self.FRAME)
        