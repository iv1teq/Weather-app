import PyQt6.QtWidgets as widgets 
import json
from PyQt6.QtGui import QPixmap
import PyQt6.QtCore as core
from PyQt6.QtGui import QPixmap
import datetime
from .search import Search
from PyQt6.QtCore import Qt
from .hour_forecast import Hour_forecast
class RightArea(widgets.QFrame):
    def __init__(self, parent: None, search, card, main_window):
        super().__init__(parent)

        self.data = None
        self.search = search
        self.card = card
        
        self.LAYOUT = widgets.QGridLayout()
        # self.LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.LAYOUT.setContentsMargins(10,10,10,10)
        self.LAYOUT.setSpacing(10)

        self.HEADER_LAYOUT = widgets.QVBoxLayout()
        self.RIGHT_LAYOUY = widgets.QVBoxLayout()
        self.RIGHT_LAYOUY.setSpacing(10)
        self.LEFT_LAYOUT = widgets.QVBoxLayout()
        self.TOP_LAYOUT = widgets.QHBoxLayout()
        self.TOP_LAYOUT.setSpacing(0)
        self.TOP_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        self.ICON_TEMP_LAYOUT = widgets.QHBoxLayout()
        self.MINMAX_LAYOUT = widgets.QHBoxLayout()
        
        self.DAY_LAYOUT = widgets.QHBoxLayout()
        self.CLOCK_LAYOUT = widgets.QGridLayout()
        
        self.MINMAX_LAYOUT.setSpacing(0)
        
        
        
        
        self.setLayout(self.LAYOUT)        
        self.LAYOUT.addLayout(self.HEADER_LAYOUT, 0, 0, alignment = core.Qt.AlignmentFlag.AlignTop)
        self.HEADER_LAYOUT.addWidget(self.search)


        card.clicked.connect(self.update_text)

        self.left_frame = widgets.QFrame(self)
        self.LAYOUT.addWidget(self.left_frame, 1, 0)
        self.left_frame.setMinimumHeight(300)
        self.left_frame.setMinimumWidth(int(main_window.width() / 3))    
        self.left_frame.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding )
        
        self.left_frame.setStyleSheet('background-color: rgba(0, 0, 0, 50); border-radius: 10px ;  ')
        
        
        self.left_frame.setLayout(self.LEFT_LAYOUT)
        

        
        self.right_frame = widgets.QFrame(self)
        self.LAYOUT.addWidget(self.right_frame, 1, 1)
        self.right_frame.setMinimumHeight(self.left_frame.height())
        self.right_frame.setMinimumWidth(self.left_frame.width())  
        self.right_frame.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding )
        # self.right_frame.setFixedSize(500, 500)
        
        self.right_frame.setStyleSheet('background-color: rgba(0, 0, 0, 50) ; border-radius: 10px ;')

        self.LAYOUT.addLayout(self.HEADER_LAYOUT, 0 ,0 )

        self.LEFT_LAYOUT.addLayout(self.TOP_LAYOUT)

        container2 = widgets.QFrame()
        container2.setFixedSize(self.left_frame.width(), 50 )
        container2.setStyleSheet('background-color: None;' \
        'border-radius: 0;  ' \
        'padding-bottom: 5px; ' \
        'border-bottom: 2px solid rgba(255, 255, 255, 50);   ' \
        'border-top: none;border-left: none;border-right: none;')


        self.geo_icon = widgets.QLabel(container2)
        self.geo_icon.setGeometry(0, 2, container2.width(), container2.height())
        self.geo_icon.setStyleSheet('background-color: None ; ' )
        geo_pix = QPixmap('media/Vector.png')
        self.geo_icon.setPixmap(geo_pix)
        
        
        
        self.top_label = widgets.QLabel(container2, text = 'Поточна позицiя')
        self.top_label.setGeometry(20,0, container2.width(), container2.height())
        self.top_label.setStyleSheet('border-radius: 0; font-size: 20px; font-weight: bold; background-color: None;' \
        'padding-bottom: 5px; ' \
        'border-bottom: 0px;   ' \
        'border-top: none;border-left: none;border-right: none; ')
        self.LEFT_LAYOUT.addWidget(container2, alignment = core.Qt.AlignmentFlag.AlignTop)
        




        self.city_label = widgets.QLabel(text = self.search.city) 
        self.city_label.setStyleSheet("font-size: 70px;font-weight: bold;  background-color: None")
        self.LEFT_LAYOUT.addWidget(self.city_label, alignment=core.Qt.AlignmentFlag.AlignHCenter)
        
        self.LEFT_LAYOUT.addLayout(self.ICON_TEMP_LAYOUT)
        container4 = widgets.QFrame()
        container4.setFixedSize(300,150)
        container4.setStyleSheet('background-color: None')

        self.WEATHER_ICON = widgets.QLabel(container4)
        self.WEATHER_ICON.setFixedSize(100,100)
        self.WEATHER_ICON.setGeometry(0, 20, container4.width(), container4.height())
        self.WEATHER_PIX = QPixmap('')
        self.WEATHER_ICON.setPixmap(self.WEATHER_PIX)
        self.WEATHER_ICON.setStyleSheet('background-color: None')


        self.temp_label = widgets.QLabel(container4) 
        self.temp_label.setStyleSheet("font-size: 100px; font-weight: bold; background-color: rgba(0, 0, 0, 0)")
        self.temp_label.setGeometry(130, 0, container4.width(), container4.height())
        self.ICON_TEMP_LAYOUT.addWidget(container4)

        self.weather_label = widgets.QLabel() 
        self.weather_label.setStyleSheet("font-size: 40px; font-weight: bold; background-color: None")
        self.LEFT_LAYOUT.addWidget(self.weather_label, alignment=core.Qt.AlignmentFlag.AlignHCenter)


        self.min_max_label = widgets.QLabel() 
        self.min_max_label.setStyleSheet("font-size: 20px; background-color: rgba(0, 0, 0, 0)")
        self.MINMAX_LAYOUT.addWidget(self.min_max_label, alignment=core.Qt.AlignmentFlag.AlignHCenter)
        
        self.LEFT_LAYOUT.addLayout(self.MINMAX_LAYOUT)
        
        
        self.right_frame.setLayout(self.RIGHT_LAYOUY)
        container3 = widgets.QFrame()
        container3.setFixedSize(self.left_frame.width(), 50 )
        container3.setStyleSheet('background-color: None;' \
        'border-radius: 0;  ' \
        'padding-bottom: 5px; ' \
        'border-bottom: 2px solid rgba(255, 255, 255, 50);   ' \
        'border-top: none;border-left: none;border-right: none;')

        self.TODAY_LABEL = widgets.QLabel(container3, text = "Сьогодні")
        self.TODAY_LABEL.setGeometry(0, 0, container3.width(), container3.height())
        self.TODAY_LABEL.setStyleSheet("border-radius:0px; font-weight: bold; font-size: 20px; background-color: rgba(0, 0, 0, 0);border-bottom: 0px ")
        self.RIGHT_LAYOUY.addWidget(container3, alignment=core.Qt.AlignmentFlag.AlignTop)
        
        self.RIGHT_LAYOUY.addLayout(self.DAY_LAYOUT)
        
        
        
        
        
        self.RIGHT_LAYOUY.addLayout(self.CLOCK_LAYOUT)
        
        
        
        
        now = datetime.datetime.now()
        weekday_number = now.weekday()
        days = ["Понеділок", "Вівторок", "Середа", "Четвер", "П’ятниця", "Субота", "Неділя"]
        self.weekday = days[weekday_number]
        self.date = now.date()
        self.WEEK_DAY = widgets.QLabel(text = self.weekday)

        self.DAY_LAYOUT.addWidget(self.WEEK_DAY, alignment=core.Qt.AlignmentFlag.AlignTop)
        self.DATE_LABEL = widgets.QLabel(text = str(self.date))

        self.DAY_LAYOUT.addWidget(self.DATE_LABEL, alignment=core.Qt.AlignmentFlag.AlignRight | core.Qt.AlignmentFlag.AlignTop)


        container = widgets.QFrame()
        container.setFixedSize(200, 200)  # размер контейнера
        container.setStyleSheet("background: none;")


        self.image_time = widgets.QLabel(container)
        self.image_time.setStyleSheet('background-color: rgba(0, 0, 0, 0)')
        self.pixmap_time = QPixmap("media/time.png")

        self.image_time.setPixmap(self.pixmap_time)
        self.image_time.setGeometry(0, 0, container.width(), container.height())
        self.image_time.setScaledContents(True) 
        

        
        self.time_label = widgets.QLabel(container)
        self.time_label.setStyleSheet('font-size: 40px; font-weight: bold; background-color: rgba(0, 0, 0, 0)')
        self.time_label.setGeometry(0, 0, container.width(), container.height())
        self.time_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.RIGHT_LAYOUY.addWidget(container, alignment=core.Qt.AlignmentFlag.AlignCenter)
        


        self.DATE_LABEL.setStyleSheet("font-size: 30px; font-weight: bold;  background-color: rgba(0, 0, 0, 0)")
        self.WEEK_DAY.setStyleSheet("font-size: 30px; font-weight: bold;  background-color: rgba(0, 0, 0, 0)")
        


        self.bottom1 = widgets.QFrame()
        self.botom1_layot = widgets.QVBoxLayout()
        self.bottom1.setLayout(self.botom1_layot)
        self.bottom1.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding )
        self.bottom1.setStyleSheet('background-color: rgba(0,0,0,50); border-radius: 10px')
        self.LAYOUT.addWidget(self.bottom1, 2, 0, 1, 0)
        
        self.bottom2 = widgets.QFrame()
        self.bottom2.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding )
        self.bottom2.setStyleSheet('background-color: rgba(0,0,0,50); border-radius: 10px')
        self.LAYOUT.addWidget(self.bottom2, 3, 0, 1, 0)
        self.HOUR_FORECAST = Hour_forecast(parent=self.bottom1)
        self.botom1_layot.addWidget(self.HOUR_FORECAST)
        

        
    def update_text(self):
        pass
    def update_data(self, data):
        self.data = data
        if not data or "list" not in data:
            return

        city_name = data["city"]["name"]
        temp = round(data["list"][0]["main"]["temp"])
        weather = data["list"][0]["weather"][0]["description"]
        min = data["list"][0]["main"]["temp_min"]
        max = data["list"][0]["main"]["temp_max"]
        icon = data["list"][0]["weather"][0]["icon"]
        

        # просто меняем текст виджетов
        self.city_label.setText(city_name)
        self.temp_label.setText(f"{temp}°")
        self.weather_label.setText(weather)
        self.min_max_label.setText(f"min: {round(min)}°, max: {round(max)}°")
        
        
        self.WEATHER_PIX = QPixmap(f'media/weather_icons/{icon}.png')  # например "01d.png"
        self.WEATHER_ICON.setPixmap(self.WEATHER_PIX)

        # обновляем время по часовому поясу города
        tz = datetime.timezone(datetime.timedelta(seconds=data["city"]["timezone"]))
        self.time_label.setText(datetime.datetime.now(tz).strftime("%H:%M"))
        
        self.HOUR_FORECAST.update_data(data = data )



