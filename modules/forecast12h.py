import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui


class Forecast12(widgets.QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSizePolicy(widgets.QSizePolicy.Policy.Expanding, widgets.QSizePolicy.Policy.Expanding)
        self.setStyleSheet('background-color: transparent')
        self.setObjectName("forecast12h")
        self.MAIN_LAYOUT = widgets.QVBoxLayout(self)
        self.MAIN_LAYOUT.setSpacing(15)
        self.MAIN_LAYOUT.setContentsMargins(5, 5, 5, 5)

        # заголовок
        self.LABEL_TEXT = widgets.QLabel()
        self.LABEL_TEXT.setStyleSheet("font-size: 40px; font-weight: bold; background-color: transparent;")
        self.MAIN_LAYOUT.addWidget(self.LABEL_TEXT)

        # underline
        underline = widgets.QFrame()
        underline.setFixedHeight(2)
        underline.setSizePolicy(widgets.QSizePolicy.Policy.Expanding, widgets.QSizePolicy.Policy.Fixed)
        underline.setStyleSheet('background-color: rgba(255, 255, 255, 30);')
        self.MAIN_LAYOUT.addWidget(underline)

        # иконки погоды над графиком
        self.ICONS_LAYOUT = widgets.QHBoxLayout()
        self.ICONS_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        self.ICONS_LAYOUT.setSpacing(5)
        self.MAIN_LAYOUT.addLayout(self.ICONS_LAYOUT)

        # нижняя часть: график + температура справа
        self.BOTTOM_LAYOUT = widgets.QHBoxLayout()
        self.BOTTOM_LAYOUT.setSpacing(5)
        self.BOTTOM_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.MAIN_LAYOUT.addLayout(self.BOTTOM_LAYOUT)

        # график с сеткой
        self.GRAPH_FRAME = widgets.QFrame()
        self.GRAPH_FRAME.setStyleSheet("""
            QFrame {
                border-image: url(media/grid.png);
                border-radius: 10px;
            }
        """)
        self.GRAPH_FRAME.setSizePolicy(widgets.QSizePolicy.Policy.Expanding, widgets.QSizePolicy.Policy.Expanding)

        self.GRAPH_LAYOUT = widgets.QHBoxLayout(self.GRAPH_FRAME)
        self.GRAPH_LAYOUT.setSpacing(10)
        self.GRAPH_LAYOUT.setContentsMargins(5, 5, 5, 5)
        self.GRAPH_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignBottom | core.Qt.AlignmentFlag.AlignLeft)
        self.BOTTOM_LAYOUT.addWidget(self.GRAPH_FRAME)

        # температурные метки справа
        self.TEMP_FRAME = widgets.QFrame()
        self.TEMP_FRAME.setStyleSheet("background-color: transparent;")
        self.TEMP_FRAME.setSizePolicy(widgets.QSizePolicy.Policy.Fixed, widgets.QSizePolicy.Policy.Expanding)
        self.TEMP_LAYOUT = widgets.QVBoxLayout(self.TEMP_FRAME)
        self.TEMP_LAYOUT.setContentsMargins(5, 0, 0, 0)
        self.TEMP_LAYOUT.setSpacing(0)
        self.TEMP_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignRight)
        self.BOTTOM_LAYOUT.addWidget(self.TEMP_FRAME)

        self.retranslateUi()

    def retranslateUi(self):
        self.LABEL_TEXT.setText(
            self.tr("Forecast for next 12 hours")
        )
    def changeEvent(self, event):
        if event.type() == core.QEvent.Type.LanguageChange:
            self.retranslateUi()

        super().changeEvent(event)
    
    def update_data(self, data):
        if not data or "list" not in data:
            return

        # очистка
        for layout in [self.TEMP_LAYOUT, self.ICONS_LAYOUT, self.GRAPH_LAYOUT]:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        # температурные метки справа
        for text in ["25°", "20°", "15°", "10°", "5°", "0°", "-5°", "-10°"]:
            label = widgets.QLabel(text=text)
            label.setFixedWidth(35)
            label.setStyleSheet("background-color: transparent; font-size: 12px;")
            self.TEMP_LAYOUT.addWidget(label)

        # иконки погоды
        for i in range(min(len(data["list"]), 38)):
            icon = data["list"][i]["weather"][0]["icon"]
            pixmap = gui.QPixmap(f'media/white_weather/{icon}.png')
            icon_label = widgets.QLabel()
            icon_label.setPixmap(pixmap)
            icon_label.setStyleSheet("background-color: transparent;")
            self.ICONS_LAYOUT.addWidget(icon_label)

        # столбики графика
        for hour_data in data["list"][:40]:
            temperature = int(hour_data["main"]["temp"])
            height = 60 if temperature == 0 else int(temperature + 60)

            column = widgets.QFrame()
            column.setSizePolicy(widgets.QSizePolicy.Policy.Expanding, widgets.QSizePolicy.Policy.Fixed)
            column.setFixedHeight(height)
            column.setStyleSheet("background-color: qlineargradient(x1:0, y1:1, x2:1, y2:0, stop:0 #87CEFA, stop:1 #FFDF56);")
            self.GRAPH_LAYOUT.addWidget(column, alignment=core.Qt.AlignmentFlag.AlignBottom)