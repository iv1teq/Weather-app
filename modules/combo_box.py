import PyQt6.QtWidgets as widgets
import requests
import json
from PyQt6.QtCore import pyqtSignal

url = 'https://countriesnow.space/api/v0.1/countries'

# кэш данных — загружается один раз на весь модуль
_data_dict = None


def get_data():
    global _data_dict
    if _data_dict is not None:
        return _data_dict
    try:
        response = requests.get(url, timeout=10)
        _data_dict = response.json()
        with open("static/json/citys_data.json", mode="w", encoding='utf-8') as file:
            json.dump(obj=_data_dict, fp=file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        # fallback — читаем из кэша
        try:
            with open("static/json/citys_data.json", encoding='utf-8') as f:
                _data_dict = json.load(f)
        except Exception as e2:
            print(f"Ошибка чтения кэша: {e2}")
            _data_dict = {"data": []}
    return _data_dict


class Search_listwidget(widgets.QListWidget):
    country_selected = pyqtSignal(str)

    def __init__(self, parent, search, width):
        super().__init__(parent)
        self.search = search
        self.cities = []
        self.countries = []
        self._signals_connected = False
        self._selected_country = None

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
        self.data_dict = get_data()


    # ОБРАБОТКА КЛИКОВ

    def on_city_clicked(self, item):
        try:
            self.search.blockSignals(True)
            self.search.setText(item.text())
            self.search.blockSignals(False)
            self.search.clearFocus()
            self.hide()
        except Exception as e:
            print(f"on_city_clicked error: {e}")

    def on_country_clicked(self, item):
        try:
            self.search.blockSignals(True)
            self.search.setText(item.text())
            self.search.blockSignals(False)
            self.search.clearFocus()
            self.hide()
            self._selected_country = item.text()
            self.country_selected.emit(item.text())
        except Exception as e:
            print(f"on_country_clicked error: {e}")


    # ПОДКЛЮЧЕНИЕ СИГНАЛОВ

    def cities_funk(self):
        if not self._signals_connected:
            self.itemClicked.connect(self.on_city_clicked)
            self._signals_connected = True

    def countries_funk(self):
        self.load_countries()
        if not self._signals_connected:
            self.itemClicked.connect(self.on_country_clicked)
            self._signals_connected = True


    # ЗАГРУЗКА ДАННЫХ

    def load_cities(self):
        self.cities = []
        for country in self.data_dict['data']:
            for city in country['cities']:
                self.cities.append(city)
        self.cities = sorted(self.cities)

    def load_countries(self):
        self.countries = []
        for country in self.data_dict['data']:
            self.countries.append(country['country'])
        self.countries = sorted(self.countries)

    def load_cities_by_country(self, country_name):
        # загружаем города только выбранной страны
        self.cities = []
        for country in self.data_dict['data']:
            if country['country'].lower() == country_name.lower():
                self.cities = sorted(country['cities'])
                break
        self.clear()


    # ФИЛЬТРАЦИЯ

    def filter_cities(self, text):
        self.clear()
        if not text or not self.cities:
            return
        filtered = [c for c in self.cities if c.lower().startswith(text.lower())]
        self.addItems(filtered[:15])

    def filter_countries(self, text):
        self.clear()
        if not text:
            return
        filtered = [c for c in self.countries if c.lower().startswith(text.lower())]
        self.addItems(filtered[:15])