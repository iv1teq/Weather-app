import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets

from .app import app_obj
from .title_bar import Title_bar
from utils import api_request
from .left_area import LeftArea
from .search import Search






class MainWindow(widgets.QMainWindow):
    def __init__(self, window_width: int, window_height: int):
        widgets.QMainWindow.__init__(self)

        self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)
        
        self.WINDOW_WIDTH = window_width
        self.WINDOW_HEIGHT = window_height
        
        self.SCREEN = app_obj.primaryScreen()
        self.SCREEN_SIZE = self.SCREEN.size()
        
        self.SCREEN_WIDTH = self.SCREEN_SIZE.width()
        self.SCREEN_HEIGHT = self.SCREEN_SIZE.height()
        
        self.CENTER_X = (self.SCREEN_WIDTH // 2) - (self.WINDOW_WIDTH // 2)
        self.CENTER_Y = (self.SCREEN_HEIGHT // 2) - (self.WINDOW_HEIGHT // 2)
        
        # self.setGeometry(self.CENTER_X, self.CENTER_Y, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.resize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.move(self.CENTER_X, self.CENTER_Y)
        
        # Делает фон всего окна прозрачным, чтобы закругление было видно
        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)

# Центральный виджет 
        self.CENTRAL_WIDGET = widgets.QWidget(parent=self)
        self.setCentralWidget(self.CENTRAL_WIDGET)
        self.CENTRAL_WIDGET.setStyleSheet("""
QWidget {
    background-color: white;   
    border-radius: 10px;       
}
""")

# Настройка центрального виджета
        self.CENTRAL_WIDGET_LAYOUT = widgets.QVBoxLayout()
        self.CENTRAL_WIDGET_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.CENTRAL_WIDGET_LAYOUT.setSpacing(0)
        self.CENTRAL_WIDGET.setLayout(self.CENTRAL_WIDGET_LAYOUT)

# TITLE_BAR добавляем в центральный виджет
        self.TITLE_BAR = Title_bar(self.CENTRAL_WIDGET, width=self.WINDOW_WIDTH)
        self.CENTRAL_WIDGET_LAYOUT.addWidget(self.TITLE_BAR)
# self.WINDOW_WIDTH, content_frame_height)
# CONTENT_FRAME — все окно без titlebar
        self.CONTENT_FRAME = widgets.QFrame(self.CENTRAL_WIDGET)
        content_frame_height = self.WINDOW_HEIGHT - self.TITLE_BAR.height()
        self.CONTENT_FRAME.setSizePolicy(widgets.QSizePolicy.Policy.Expanding, widgets.QSizePolicy.Policy.Expanding)
        self.CONTENT_FRAME_LAYOUT = widgets.QHBoxLayout()
        self.CONTENT_FRAME_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.CONTENT_FRAME_LAYOUT.setSpacing(0)
        self.CONTENT_FRAME.setLayout(self.CONTENT_FRAME_LAYOUT)


# LeftArea внутри CONTENT_FRAME 
        self.LEFTAREA = LeftArea(self.CONTENT_FRAME, 
                                main_window=self
                                )
        
#Right Area
        self.RIGHTAREA = widgets.QFrame(self.CONTENT_FRAME)
        self.RIGHTAREA.setSizePolicy(
    widgets.QSizePolicy.Policy.Expanding,
    widgets.QSizePolicy.Policy.Expanding
)

# Добавляем LEFTAREA в CONTENT_FRAME
        self.CONTENT_FRAME_LAYOUT.addWidget(self.LEFTAREA, 1 )
        self.CONTENT_FRAME_LAYOUT.addWidget(self.RIGHTAREA, 3)
        self.CONTENT_FRAME_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignLeft)

# Фон CONTENT_FRAME — градиент, углы 
        self.CONTENT_FRAME.setStyleSheet("""
QFrame {
    background: qlineargradient(
        x1:0, y1:1,        
        x2:1, y2:0,        
        stop:0 #87CEFA,      
        stop:1 #FFDF56 
    );
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px; 
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}
""")

# Добавляем CONTENT_FRAME в центральный виджет
        self.CENTRAL_WIDGET_LAYOUT.addWidget(self.CONTENT_FRAME)
        
        

        
        


        
















        # self.FRAME = widgets.QFrame(parent = self.CONTENT_FRAME)
        # self.FRAME.setStyleSheet("background-color: red; ")
        # self.FRAME.setFixedSize(788, 197)
        # self.CONTENT_FRAME_LAYOUT.addWidget(self.FRAME)

        # self.FRAME_LAYOUT = widgets.QVBoxLayout()
        # self.FRAME.setLayout(self.FRAME_LAYOUT)
        
        # self.CONTENT_FRAME_LAYOUT.addWidget(self.FRAME)
        
        # self.FRAME1 = widgets.QFrame(parent = self.FRAME)
        # self.FRAME1.setStyleSheet("background-color: green; ")
        # self.FRAME1.setFixedSize(730, 24)
        
        # self.FRAME1_LAYOUT = widgets.QHBoxLayout()
        # self.FRAME1.setLayout(self.FRAME1_LAYOUT)
        
        # self.FRAME_LAYOUT.addWidget(self.FRAME1)
        
        # self.FRAME2 = widgets.QFrame(parent = self.FRAME)
        # self.FRAME2.setStyleSheet("background-color: blue; ")
        # self.FRAME2.setFixedWidth(730)
        
        # self.FRAME2_LAYOUT = widgets.QHBoxLayout()
        # self.FRAME2_LAYOUT.setContentsMargins(0, 0, 0, 0)
        # self.FRAME2_LAYOUT.setSpacing(10)
        # self.FRAME2_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        # self.FRAME2.setLayout(self.FRAME2_LAYOUT)
        
        # self.FRAME_LAYOUT.addWidget(self.FRAME2)
        
        # self.TEMPERATURE_GRAPH_FRAME = widgets.QFrame(parent = self.FRAME2)
        # self.TEMPERATURE_GRAPH_FRAME.setMaximumSize(727, 136)
        
        # self.TEMPERATURE_GRAPH_FRAME_LAYOUT = widgets.QHBoxLayout()
        # self.TEMPERATURE_GRAPH_FRAME_LAYOUT.setContentsMargins(0, 0, 0, 0)
        # self.TEMPERATURE_GRAPH_FRAME_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignBottom)
        # self.TEMPERATURE_GRAPH_FRAME.setLayout(self.TEMPERATURE_GRAPH_FRAME_LAYOUT)
        
        # self.FRAME2_LAYOUT.addWidget(self.TEMPERATURE_GRAPH_FRAME)
        
        # data_dict = api_request("Miami")
        
        # for hour_data in data_dict["list"]:
        #     temperature = int(hour_data["main"]["temp"])
            
        #     height = 0
            
        #     if temperature < 0 :
        #         height = (temperature * -2)  + 30
        #     elif temperature == 0:
        #         height = 30
        #     else:
        #         height = temperature * 2 
            
        #     self.COLUMN = widgets.QFrame(self.TEMPERATURE_GRAPH_FRAME)
        #     self.COLUMN.setFixedSize(core.QSize(8, height))
        #     self.COLUMN.setStyleSheet("background-color: gray; ")
        #     self.TEMPERATURE_GRAPH_FRAME_LAYOUT.addWidget(self.COLUMN, alignment = core.Qt.AlignmentFlag.AlignBottom)


