import PyQt6.QtWidgets as widgets 
import json
from PyQt6.QtGui import QPixmap
import PyQt6.QtCore as core
from PyQt6.QtGui import QPixmap
import datetime
from .search import Search
from PyQt6.QtCore import Qt
from .hour_forecast import Hour_forecast
from .forecast12h import Forecast12
import PyQt6.QtGui as gui
from .combo_box import Search_combobox

class RightArea(widgets.QFrame):
        def __init__(self, parent: None, search, card, main_window):
                super().__init__(parent)

                self.data = None
                self.search = search
                self.card = card
                
        
                # self.combobox.citys_request()

                self.LAYOUT = widgets.QGridLayout()
                self.LAYOUT.setRowStretch(2, 1)
                self.LAYOUT.setRowStretch(3, 1)

                self.LAYOUT.setColumnStretch(0, 1)
                self.LAYOUT.setColumnStretch(1, 1)
                
                # self.LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)
                self.LAYOUT.setContentsMargins(10,10,10,10)
                self.LAYOUT.setSpacing(10)

                self.HEADER_LAYOUT = widgets.QHBoxLayout()
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
                
                #search
                self.SEARCH_LAYOUT = widgets.QHBoxLayout()


                self.MINMAX_LAYOUT.setSpacing(0)
                self.setLayout(self.LAYOUT)        
                self.LAYOUT.addLayout(self.HEADER_LAYOUT, 0, 0, 1, 0, alignment = core.Qt.AlignmentFlag.AlignTop)
                


                # card.clicked.connect(self.update_text)

                #top left frame
                self.left_frame = widgets.QFrame(self)
                self.LAYOUT.addWidget(self.left_frame, 1, 0)
                self.left_frame.setMinimumHeight(int(main_window.width() / 5))
                self.left_frame.setMinimumWidth(int(main_window.width() / 5))    
                self.left_frame.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding )
                
                self.left_frame.setStyleSheet('background-color: rgba(0, 0, 0, 50); border-radius: 10px ;  ')
                
                
                self.left_frame.setLayout(self.LEFT_LAYOUT)
                

                #top right frame
                self.right_frame = widgets.QFrame(self)
                self.LAYOUT.addWidget(self.right_frame, 1, 1)
                self.right_frame.setMinimumHeight(self.left_frame.height())
                self.right_frame.setMinimumWidth(self.left_frame.width())  
                self.right_frame.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding )
                
                self.right_frame.setStyleSheet('background-color: rgba(0, 0, 0, 50) ; border-radius: 10px ;')

                self.LAYOUT.addLayout(self.HEADER_LAYOUT, 0 ,0 )
                self.right_frame.setLayout(self.RIGHT_LAYOUY)
                self.LEFT_LAYOUT.addLayout(self.TOP_LAYOUT)


                #container for geo icon and text
                container2 = widgets.QFrame()
                container2.setFixedSize(1000, 50 )
                container2.setStyleSheet('background-color: None;' \
                'border-radius: 0;  ' \
                'padding-bottom: 5px; ' \
                'border-bottom: 2px solid rgba(255, 255, 255, 50);   ' \
                'border-top: none;border-left: none;border-right: none;')

                #geo icon
                self.geo_icon = widgets.QLabel(container2)
                self.geo_icon.setGeometry(0, 2, container2.width(), container2.height())
                self.geo_icon.setStyleSheet('background-color: None ; ' )
                geo_pix = QPixmap('media/Vector.png')
                self.geo_icon.setPixmap(geo_pix)
                
                
                #label left frame
                self.top_label = widgets.QLabel(container2, text = 'Поточна позицiя')
                self.top_label.setGeometry(20,0, container2.width(), container2.height())
                self.top_label.setStyleSheet('border-radius: 0; font-size: 20px; font-weight: bold; background-color: None;' \
                'padding-bottom: 5px; ' \
                'border-bottom: 0px;   ' \
                'border-top: none;border-left: none;border-right: none; ')
                self.LEFT_LAYOUT.addWidget(container2, alignment = core.Qt.AlignmentFlag.AlignTop)
                
                #city left frame
                self.city_label = widgets.QLabel(text = self.search.city) 
                self.city_label.setStyleSheet("font-size: 70px;font-weight: bold;  background-color: None")
                self.LEFT_LAYOUT.addWidget(self.city_label, alignment=core.Qt.AlignmentFlag.AlignHCenter)
                
                self.LEFT_LAYOUT.addLayout(self.ICON_TEMP_LAYOUT)

                #container for weather icon and temp label
                container4 = widgets.QFrame()
                container4.setFixedSize(300,150)
                container4.setStyleSheet('background-color: None')
                #weather icon
                self.WEATHER_ICON = widgets.QLabel(container4)
                self.WEATHER_ICON.setFixedSize(100,100)
                self.WEATHER_ICON.move(0, 20)
                self.WEATHER_PIX = QPixmap('')
                self.WEATHER_ICON.setPixmap(self.WEATHER_PIX)
                self.WEATHER_ICON.setStyleSheet('background-color: None')

                #temp label
                self.temp_label = widgets.QLabel(container4) 
                self.temp_label.setStyleSheet("font-size: 100px; font-weight: bold; background-color: rgba(0, 0, 0, 0)")
                self.temp_label.setGeometry(130, 0, container4.width(), container4.height())
                self.ICON_TEMP_LAYOUT.addWidget(container4)
                #icl left frame
                self.weather_label = widgets.QLabel() 
                self.weather_label.setStyleSheet("font-size: 40px; font-weight: bold; background-color: None")
                self.LEFT_LAYOUT.addWidget(self.weather_label, alignment=core.Qt.AlignmentFlag.AlignHCenter)

                self.min_max_label = widgets.QLabel() 
                self.min_max_label.setStyleSheet("font-size: 20px; background-color: rgba(0, 0, 0, 0)")
                self.MINMAX_LAYOUT.addWidget(self.min_max_label, alignment=core.Qt.AlignmentFlag.AlignHCenter)
                
                self.LEFT_LAYOUT.addLayout(self.MINMAX_LAYOUT)
                
                
                
                container3 = widgets.QFrame()
                container3.setFixedSize(1000, 50 )
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
                
                #settings button
                self.settings_button = widgets.QPushButton()
                self.settings_button.setFixedSize(50, 50)
                self.settings_button.setStyleSheet('background: rgba(0,0,0,50)')
                
                self.icon_settings = gui.QIcon('media/settings.png')
                self.settings_button.setIcon(self.icon_settings)

                self.HEADER_LAYOUT.addWidget(self.settings_button)
                #settings label

                self.settings_label = widgets.QLabel(text = 'Settings')
                self.settings_label.setStyleSheet('font-size: 40px; font-weight: bold; background-color: rgba(0, 0, 0, 0)')
                self.HEADER_LAYOUT.addWidget(self.settings_label)
                #search frame 
                self.SEARCH_WIDGET = widgets.QFrame(self)
                
                self.SEARCH_WIDGET.setMinimumWidth(400)
                self.SEARCH_WIDGET.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding)
                self.SEARCH_WIDGET.setStyleSheet("background-color: rgba(0, 0, 0, 60); border-radius: 10px; border: 2px solid white;")
                self.SEARCH_IMAGE = widgets.QLabel(self.SEARCH_WIDGET)
                pixmap_search = QPixmap("media/search_image.png")
                self.SEARCH_IMAGE.setPixmap(pixmap_search)
                self.CROSS = widgets.QLabel(self.SEARCH_WIDGET)
                pixmap_cross = QPixmap("media/clear.png")
                self.CROSS.setPixmap(pixmap_cross)
                self.SEARCH_IMAGE.setStyleSheet("background-color: None; border: 0px ;")
                self.CROSS.setStyleSheet("background-color: None;  border: 0px ;")
                self.search.setStyleSheet('border: 0px; background-color: rgba(0, 0, 0, 0)')
                self.HEADER_LAYOUT.addWidget(self.SEARCH_WIDGET, alignment=core.Qt.AlignmentFlag.AlignRight)
                self.SEARCH_WIDGET.setLayout(self.SEARCH_LAYOUT)
                self.SEARCH_LAYOUT.addWidget(self.SEARCH_IMAGE)
                self.SEARCH_LAYOUT.addWidget(self.search)
                self.SEARCH_LAYOUT.addWidget(self.CROSS)
                self.HEADER_LAYOUT.addWidget(self.SEARCH_WIDGET, alignment=core.Qt.AlignmentFlag.AlignRight)
                #combobox

                self.combobox = Search_combobox(self, search = self.search, width = self.SEARCH_WIDGET.width() )
                # self.HEADER_LAYOUT.addWidget(self.combobox)
                self.combobox.hide()
                self.search.textChanged.connect(self.combobox_funk)

                self.bottom1 = widgets.QFrame()
                self.botom1_layot = widgets.QVBoxLayout()
                self.bottom1.setLayout(self.botom1_layot)
                self.bottom1.setMinimumHeight(200)
                self.bottom1.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding )
                self.bottom1.setStyleSheet('background-color: rgba(0,0,0,50); border-radius: 10px')
                self.HOUR_FORECAST = Hour_forecast(parent=self.bottom1)
                self.LAYOUT.addWidget(self.bottom1, 2, 0, 1, 0)
                self.botom1_layot.addWidget(self.HOUR_FORECAST)
                
                self.bottom2 = widgets.QFrame()
                self.bottom2_layout = widgets.QVBoxLayout()
                self.bottom2.setLayout(self.bottom2_layout)
                self.bottom2.setStyleSheet('background-color: rgba(0,0,0,50); border-radius: 10px')
                self.LAYOUT.addWidget(self.bottom2, 3, 0, 1, 2)
                self.bottom2.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding )
                self.FORECAST12 = Forecast12(parent = self.bottom2)
                self.bottom2_layout.addWidget(self.FORECAST12)

        def resizeEvent(self, event):
                super().resizeEvent(event)
                self.update_combobox_position()

        def update_combobox_position(self):
                # Получаем позицию SEARCH_WIDGET относительно RightArea
                pos = self.SEARCH_WIDGET.mapTo(self, self.SEARCH_WIDGET.rect().bottomLeft())
                self.combobox.move(pos.x(), pos.y() + 5)  # +5 небольшой отступ


        def update_data(self, data):
                self.data = data
                if not data or "list" not in data:
                        return

                self.city_name = data["city"]["name"]
                self.temp = round(data["list"][0]["main"]["temp"])
                self.weather = data["list"][0]["weather"][0]["description"]
                self.min = data["list"][0]["main"]["temp_min"]
                self.max = data["list"][0]["main"]["temp_max"]
                self.icon = data["list"][0]["weather"][0]["icon"]
                

                # просто меняем текст виджетов
                self.city_label.setText(self.city_name)
                self.temp_label.setText(f"{self.temp}°")
                self.weather_label.setText(self.weather)
                self.min_max_label.setText(f"min: {round(self.min)}°, max: {round(self.max)}°")
                
                
                self.WEATHER_PIX = QPixmap(f'media/weather_icons/{self.icon}.png')  # например "01d.png"
                self.WEATHER_ICON.setPixmap(self.WEATHER_PIX)

                # обновляем время по часовому поясу города
                tz = datetime.timezone(datetime.timedelta(seconds=data["city"]["timezone"]))
                self.time_label.setText(datetime.datetime.now(tz).strftime("%H:%M"))
                
                self.HOUR_FORECAST.update_data(data = data )
                self.FORECAST12.update_data(data = data)
        def combobox_funk(self):
                if self.search.text() == "":
                        self.combobox.hide()
                else:
                        self.update_combobox_position()
                        self.combobox.filter_cities(self.search.text())
                        self.combobox.raise_()
                        self.combobox.show()
                        