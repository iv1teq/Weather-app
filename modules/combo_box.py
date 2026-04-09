import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import requests
import json
from PyQt6.QtCore import pyqtSignal

url = 'https://countriesnow.space/api/v0.1/countries'

class Search_listwidget(widgets.QListWidget):
    country_selected = pyqtSignal(str)
    def __init__(self, parent, search, width):
        super().__init__(parent)
        self.search = search
        self.cities = []
        self.countries = []

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

    def on_city_clicked(self, item):
        try:
            self.search.setText(item.text())
            self.search.setFocus()
            self.hide()
        except Exception as e:
            print(f"on_city_clicked error: {e}")

    def on_country_clicked(self, item):
        try:
            self.search.setText(item.text())
            self.search.setFocus()
            self.hide()
            self.country_selected.emit(item.text())  # только для стран
        except Exception as e:
            print(f"on_country_clicked error: {e}")

    def cities_funk(self):
        self.load_cities()

        self.search.textChanged.connect(self.filter_cities)
        self.itemClicked.connect(self.on_city_clicked)

    def countries_funk(self):
        self.load_countries()

        self.search.textChanged.connect(self.filter_countries)
        self.itemClicked.connect(self.on_country_clicked)

    def load_cities(self):
        for country in self.data_dict['data']:
            for city in country['cities']:
                self.cities.append(city)

        self.cities = sorted(self.cities)
    
    def load_countries(self):
        for country in self.data_dict['data']:
            self.countries.append(country['country'])

        self.countries = sorted(self.countries)
        

    
            
    def filter_cities(self, text):
        self.clear()

        if not text:
            return

        filtered = [
            city for city in self.cities
            if city.lower().startswith(text.lower())
        ]

        self.addItems(filtered[:15])

    def filter_countries(self, text):
        self.clear()

        if not text:
            return

        filtered = [
            country for country in self.countries
            if country.lower().startswith(text.lower())
        ]

        self.addItems(filtered[:15])
    
    def load_cities_by_country(self, country_name):
        self.cities = []
        for country in self.data_dict['data']:
            if country['country'].lower() == country_name.lower():
                self.cities = sorted(country['cities'])
                break
        self.clear() 