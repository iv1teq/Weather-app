import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
from PyQt6.QtGui import QPixmap
import PyQt6.QtGui as gui
import datetime
class Hour_forecast(widgets.QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        data = None
        self.LAYOUT = widgets.QVBoxLayout()
        self.setLayout(self.LAYOUT)
        
        
        self.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding )
        
        

        self.SCROLL_AREA = widgets.QScrollArea(self)
        self.SCROLL_AREA.setWidgetResizable(True)
        self.SCROLL_AREA.setStyleSheet("border: none;")
        self.SCROLL_AREA.setStyleSheet("""
    background-color: transparent;  
    border: none;                   
""")
        self.SCROLL_FRAME = widgets.QFrame()
        self.SCROLL_LAYOUT = widgets.QHBoxLayout(self.SCROLL_FRAME)

        self.SCROLL_FRAME.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding)

        self.SCROLL_AREA.setWidget(self.SCROLL_FRAME)
        self.SCROLL_AREA.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SCROLL_AREA.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
            

        self.setStyleSheet('background-color: None')
        
    def update_data(self, data):
        if not data or "list" not in data:
            return
        temp_list = []
        weather_list = []
        
        for i in range(0, 9):
            for _ in range(3):
                temp_list.append(data["list"][i]["main"]["temp"])
                weather_list.append(data["list"][i]["weather"][0]["icon"])
        
            
        now = int(datetime.datetime.now(datetime.timezone(datetime.timedelta(seconds = data["city"]["timezone"]))).strftime("%H"))
        for hour in range(now, now+24):
            if hour == now:
                self.TIME_LABEL = widgets.QLabel(text = "now")
            else:
                self.TIME_LABEL = widgets.QLabel(text = str(hour%24))
            self.FRAME_LAYOUT = widgets.QVBoxLayout()
            self.FRAME = widgets.QFrame(self.SCROLL_FRAME)
            self.FRAME.setLayout(self.FRAME_LAYOUT)
            

            self.IMAGE_LABEL = widgets.QLabel()

            weather_pixmap = QPixmap(f"media/white_weather/{weather_list[hour%24]}.png")
            weather_pixmap = weather_pixmap.scaled(30, 30, core.Qt.AspectRatioMode.IgnoreAspectRatio, core.Qt.TransformationMode.SmoothTransformation)

            self.IMAGE_LABEL.setPixmap(weather_pixmap)
            self.TEMP_LABEL = widgets.QLabel(self.SCROLL_FRAME, text = str(round(temp_list[hour%24]))+"°")
            self.TIME_LABEL.setStyleSheet("font-size: 20px")
            self.TEMP_LABEL.setStyleSheet("font-size: 20px")
                
            
            self.FRAME_LAYOUT.addWidget(self.TIME_LABEL, alignment = core.Qt.AlignmentFlag.AlignCenter)
            self.FRAME_LAYOUT.addWidget(self.IMAGE_LABEL, core.Qt.AlignmentFlag.AlignLeft)
            self.FRAME_LAYOUT.addWidget(self.TEMP_LABEL, alignment = core.Qt.AlignmentFlag.AlignCenter)
            self.SCROLL_LAYOUT.addWidget(self.FRAME)
            

            
        weather = data["list"][0]["weather"][0]["description"]
        self.WEATHER_LABEL = widgets.QLabel(self, text = f"{weather} until the end of the day")
        self.WEATHER_LABEL.setStyleSheet("font-size: 27px; font-weight: bold")

        #underline
        underline = widgets.QFrame()
        underline.setFixedHeight(2)
        underline.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Fixed)
        underline.setStyleSheet('background-color: rgba(255, 255, 255, 30) ')

        # add to layout
        self.LAYOUT.addWidget(self.WEATHER_LABEL, alignment=core.Qt.AlignmentFlag.AlignTop)
        self.LAYOUT.addWidget(underline)
        self.LAYOUT.addWidget(self.SCROLL_AREA)

