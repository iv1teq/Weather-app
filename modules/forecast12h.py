
import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui




class Forecast12(widgets.QFrame) : 
        
        def __init__(self, parent = None  ):
            super().__init__(parent)

            self.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding)

            self.LAYOUT = widgets.QGridLayout()
            self.setStyleSheet('background-color: None')
            self.ICONS_LAYOUT = widgets.QHBoxLayout()
            self.ICONS_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
            # self.ICONS_LAYOUT.setSpacing(1)
            self.TEMP_LAYOUT = widgets.QVBoxLayout()
            self.GRAPH_LAYOUT = widgets.QHBoxLayout()
            self.GRAPH_LAYOUT.setSpacing(10)
            self.LABEL_LAYOUT = widgets.QHBoxLayout()
            
            self.setLayout(self.LAYOUT)
            
            self.LABEL_TEXT = widgets.QLabel( text="Прогноз на 12 годин")
            self.LABEL_TEXT.setStyleSheet("background-color: None; font-size: 20px;")
            self.TEMP_LAYOUT.setContentsMargins(0, 0, 0, 0)
            self.TEMP_LAYOUT.setSpacing(0)
            self.TEMP_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignRight)
            # self.TEMP_LABEL = widgets.QLabel(text = "25°\n20°\n15°\n10°\n5°\n0°\n-5°\n-10°\n")
            
            
            
            
            
            
            

            self.LAYOUT.addLayout(self.LABEL_LAYOUT, 0, 0)
            self.LAYOUT.addLayout(self.ICONS_LAYOUT, 1, 0 )
            self.LAYOUT.addLayout(self.TEMP_LAYOUT, 2, 2)
            self.LAYOUT.addLayout(self.GRAPH_LAYOUT, 2, 0)


            
            self.LABEL_LAYOUT.addWidget(self.LABEL_TEXT, alignment=core.Qt.AlignmentFlag.AlignTop)



        def update_data(self, data):
            if not data or "list" not in data:
                return
            self.tem25 = widgets.QLabel(text = "25°")
            self.tem20 = widgets.QLabel(text = "20°")
            self.tem15 = widgets.QLabel(text = "15°")
            self.tem10 = widgets.QLabel(text = "10°")
            self.temp5 = widgets.QLabel(text = '5°')
            self.temp0 = widgets.QLabel(text = '0°')
            self.temp_5 = widgets.QLabel(text = '-5°')
            self.temp_10 = widgets.QLabel(text = '-10°')
            

            self.TEMP_LAYOUT.addWidget(self.tem25)
            self.TEMP_LAYOUT.addWidget(self.tem20)
            self.TEMP_LAYOUT.addWidget(self.tem15)
            self.TEMP_LAYOUT.addWidget(self.tem10)
            self.TEMP_LAYOUT.addWidget(self.temp5)
            self.TEMP_LAYOUT.addWidget(self.temp0)
            self.TEMP_LAYOUT.addWidget(self.temp_5)
            self.TEMP_LAYOUT.addWidget(self.temp_10)
            
            for i in range(4):
                    for _ in range(3):
                        icon = data["list"][i]["weather"][0]["icon"]
                        pixmap = gui.QPixmap(f'media/weather_icons/{icon}.png')
                        icon_label = widgets.QLabel()

                    

        #                 pixmap = pixmap.scaled(
        #     70,
        #     70,
        #     core.Qt.AspectRatioMode.IgnoreAspectRatio,
        #     core.Qt.TransformationMode.SmoothTransformation
        # )
                        icon_label.setPixmap(pixmap)
                        icon_label.setStyleSheet("background-color: None")

                        self.ICONS_LAYOUT.addWidget(icon_label, core.Qt.AlignmentFlag.AlignLeft)
                    
            for hour_data in data["list"]:
                temperature = int(hour_data["main"]["temp"])
                
                
                
                if temperature == 0 :
                    height = 60
                    self.COLUMN = widgets.QFrame(self)
                    self.COLUMN.setFixedSize(core.QSize(16, height))
                    self.COLUMN.setStyleSheet("background-color: pink ; ")
                    self.GRAPH_LAYOUT.addWidget(self.COLUMN, alignment = core.Qt.AlignmentFlag.AlignBottom)
                else:
                    height = int(temperature + 60)
                    self.COLUMN = widgets.QFrame(self)
                    self.COLUMN.setFixedSize(core.QSize(12, height))
                    self.COLUMN.setStyleSheet("background-color:qlineargradient(x1:0, y1:1,x2:1, y2:0,stop:0 #87CEFA,stop:1 #FFDF56) ; ")
                    self.GRAPH_LAYOUT.addWidget(self.COLUMN, alignment = core.Qt.AlignmentFlag.AlignBottom)

            
                
