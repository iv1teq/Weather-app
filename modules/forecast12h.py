
import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui




class Forecast12(widgets.QFrame) : 
        
        def __init__(self, parent = None  ):
            super().__init__(parent)

            self.setSizePolicy(widgets.QSizePolicy.Policy.Expanding,widgets.QSizePolicy.Policy.Expanding)

            self.LAYOUT = widgets.QGridLayout()
            
            self.ICONS_LAYOUT = widgets.QHBoxLayout()
            self.TEMP_LAYOUT = widgets.QVBoxLayout()
            self.GRAPH_LAYOUT = widgets.QHBoxLayout()
            self.GRAPH_LAYOUT.setSpacing(5)
            self.LABEL_LAYOUT = widgets.QHBoxLayout()
            
            self.setLayout(self.LAYOUT)
            
            self.LABEL_TEXT = widgets.QLabel( text="Прогноз на 12 годин")
            self.LABEL_TEXT.setStyleSheet("font-size: 20px;")

            
            self.LAYOUT.addLayout(self.LABEL_LAYOUT, 0, 0)
            self.LAYOUT.addLayout(self.ICONS_LAYOUT, 1, 0 )
            self.LAYOUT.addLayout(self.TEMP_LAYOUT, 0, 2)
            self.LAYOUT.addLayout(self.GRAPH_LAYOUT, 2, 0)
            

            
            self.LABEL_LAYOUT.addWidget(self.LABEL_TEXT)



        def update_data(self, data):
            if not data or "list" not in data:
                return
            for hour_data in data["list"]:
                temperature = int(hour_data["main"]["temp"])
                
                
                
                if temperature == 0 :
                    height = 100
                    self.COLUMN = widgets.QFrame(self)
                    self.COLUMN.setFixedSize(core.QSize(8, height))
                    self.COLUMN.setStyleSheet("background-color: pink ; ")
                    self.GRAPH_LAYOUT.addWidget(self.COLUMN, alignment = core.Qt.AlignmentFlag.AlignBottom)
                else:
                    height = temperature + 100
                    self.COLUMN = widgets.QFrame(self)
                    self.COLUMN.setFixedSize(core.QSize(8, height))
                    self.COLUMN.setStyleSheet("background-color: pink ; ")
                    self.GRAPH_LAYOUT.addWidget(self.COLUMN, alignment = core.Qt.AlignmentFlag.AlignBottom)

            
                icon_label = widgets.QLabel()

                icon = data["list"][0]["weather"][0]["icon"]
                pixmap = gui.QPixmap(f'media/weather_icons/{icon}.png')
                pixmap = pixmap.scaled(
    30,
    30,
    core.Qt.AspectRatioMode.KeepAspectRatio,
    core.Qt.TransformationMode.SmoothTransformation
)
                icon_label.setPixmap(pixmap)

                self.ICONS_LAYOUT.addWidget(icon_label)
#         def clear(self, data): 
#             for hour_data in data["list"]:
#                 temperature = int(hour_data["main"]["temp"])
                
                
                
#                 if temperature == 0 :
#                     height = 100
#                     self.COLUMN = widgets.QFrame(self)
#                     self.COLUMN.setFixedSize(core.QSize(8, height))
#                     self.COLUMN.setStyleSheet("background-color: pink ; ")
#                     self.GRAPH_LAYOUT.addWidget(self.COLUMN, alignment = core.Qt.AlignmentFlag.AlignBottom)
#                 else:
#                     height = temperature + 100
#                     self.COLUMN = widgets.QFrame(self)
#                     self.COLUMN.setFixedSize(core.QSize(8, height))
#                     self.COLUMN.setStyleSheet("background-color: pink ; ")
#                     self.GRAPH_LAYOUT.addWidget(self.COLUMN, alignment = core.Qt.AlignmentFlag.AlignBottom)

            
#                 icon_label = widgets.QLabel()

#                 icon = data["list"][0]["weather"][0]["icon"]
#                 pixmap = gui.QPixmap(f'media/weather_icons/{icon}.png')
#                 pixmap = pixmap.scaled(
#     30,
#     30,
#     core.Qt.AspectRatioMode.KeepAspectRatio,
#     core.Qt.TransformationMode.SmoothTransformation
# )
#                 icon_label.setPixmap(pixmap)

#                 self.ICONS_LAYOUT.addWidget(icon_label)