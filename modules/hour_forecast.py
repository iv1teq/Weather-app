import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
from PyQt6.QtGui import QPixmap
import PyQt6.QtGui as gui
import datetime

class Hour_forecast(widgets.QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('hour_forecast')
        self._data = None
        self._translatable_labels = []  # список (label, key, args)

        self.LAYOUT = widgets.QVBoxLayout()
        self.setLayout(self.LAYOUT)

        self.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Expanding
        )

        self.SCROLL_AREA = widgets.QScrollArea(self)
        self.SCROLL_AREA.setWidgetResizable(True)
        self.SCROLL_AREA.setStyleSheet("""
            background-color: transparent;
            border: none;
        """)

        self.SCROLL_FRAME = widgets.QFrame()
        self.SCROLL_LAYOUT = widgets.QHBoxLayout(self.SCROLL_FRAME)
        self.SCROLL_FRAME.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Expanding
        )
        self.SCROLL_AREA.setWidget(self.SCROLL_FRAME)
        self.SCROLL_AREA.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SCROLL_AREA.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.WEATHER_LABEL = widgets.QLabel(self)
        self.WEATHER_LABEL.setStyleSheet("font-size: 27px; font-weight: bold")
        self.LAYOUT.addWidget(self.WEATHER_LABEL, alignment=core.Qt.AlignmentFlag.AlignTop)
        self.WEATHER_LABEL.hide()

        self.setStyleSheet('background-color: None')

    def update_data(self, data):
        if not data or "list" not in data:
            return

        self._data = data
        self._translatable_labels.clear()

        # Очищаем старые виджеты в скролле
        while self.SCROLL_LAYOUT.count():
            item = self.SCROLL_LAYOUT.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        temp_list = []
        weather_list = []

        for i in range(0, 9):
            for _ in range(3):
                temp_list.append(data["list"][i]["main"]["temp"])
                weather_list.append(data["list"][i]["weather"][0]["icon"])

        tz = datetime.timezone(datetime.timedelta(seconds=data["city"]["timezone"]))
        now = int(datetime.datetime.now(tz).strftime("%H"))

        for hour in range(now, now + 24):
            frame = widgets.QFrame(self.SCROLL_FRAME)
            frame_layout = widgets.QVBoxLayout(frame)

            # Метка времени
            time_label = widgets.QLabel()
            time_label.setStyleSheet("font-size: 20px")
            if hour == now:
                time_label.setText(self.tr("now"))
                # Запоминаем для ретрансляции
                self._translatable_labels.append((time_label, "now", None))
            else:
                time_label.setText(str(hour % 24))

            # Иконка погоды
            image_label = widgets.QLabel()
            pixmap = QPixmap(f"media/white_weather/{weather_list[hour % 24]}.png")
            pixmap = pixmap.scaled(
                30, 30,
                core.Qt.AspectRatioMode.IgnoreAspectRatio,
                core.Qt.TransformationMode.SmoothTransformation
            )
            image_label.setPixmap(pixmap)

            # Температура
            temp_label = widgets.QLabel(str(round(temp_list[hour % 24])) + "°")
            temp_label.setStyleSheet("font-size: 20px")

            frame_layout.addWidget(time_label, alignment=core.Qt.AlignmentFlag.AlignCenter)
            frame_layout.addWidget(image_label, alignment=core.Qt.AlignmentFlag.AlignCenter)
            frame_layout.addWidget(temp_label, alignment=core.Qt.AlignmentFlag.AlignCenter)
            self.SCROLL_LAYOUT.addWidget(frame)

        self._weather_description = data["list"][0]["weather"][0]["description"]
        self.WEATHER_LABEL.show()

        # Добавляем разделитель и скролл только один раз
        if self.LAYOUT.count() < 3:
            underline = widgets.QFrame()
            underline.setFixedHeight(2)
            underline.setSizePolicy(
                widgets.QSizePolicy.Policy.Expanding,
                widgets.QSizePolicy.Policy.Fixed
            )
            underline.setStyleSheet('background-color: rgba(255, 255, 255, 30)')
            self.LAYOUT.addWidget(underline)
            self.LAYOUT.addWidget(self.SCROLL_AREA)

        self.retranslateUi()

    def retranslateUi(self):
        if hasattr(self, '_weather_description'):
            self.WEATHER_LABEL.setText(
                self.tr("%1 until the end of the day").replace("%1", self._weather_description)
            )

        # Обновляем все сохранённые переводимые лейблы
        for label, key, args in self._translatable_labels:
            label.setText(self.tr(key))

    def changeEvent(self, event):
        if event.type() == core.QEvent.Type.LanguageChange:
            self.retranslateUi()
        super().changeEvent(event)