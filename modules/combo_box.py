import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import requests
import json

url = 'https://countriesnow.space/api/v0.1/countries'

class Search_listwidget(widgets.QListWidget):
    def __init__(self, parent, search, width):
        super().__init__(parent)
        self.search = search
        self.cities = []

        self.setStyleSheet("""
            QListWidget {
                background-color: rgba(0, 0, 0, 200);
                border: 1px solid white;
                border-radius: 5px;
                color: white;
                font-size: 16px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 4px;
            }
            QListWidget::item:selected {
                background-color: rgba(255, 255, 255, 50);
            }
            QListWidget::item:hover {
                background-color: rgba(255, 255, 255, 30);
            }
        """)

        self.setFixedWidth(width)

        # Загружаем данные
        response = requests.get(url)
        self.data_dict = response.json()

        with open("static/json/citys_data.json", mode="w", encoding='utf-8') as file:
            json.dump(obj=self.data_dict, fp=file, indent=4, ensure_ascii=False)

        self.load_cities()

        self.search.textChanged.connect(self.filter_cities)
        self.itemClicked.connect(self.on_item_clicked)

    def load_cities(self):
        for country in self.data_dict['data']:
            for city in country['cities']:
                self.cities.append(city)

        self.cities = sorted(self.cities)

    def on_item_clicked(self, item):
        self.search.setText(item.text())
        self.search.setFocus()


    def filter_cities(self, text):
        self.clear()

        if not text:
            return

        filtered = [
            city for city in self.cities
            if city.lower().startswith(text.lower())
        ]

        self.addItems(filtered[:15])