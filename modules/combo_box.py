import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import requests
import json

url = 'https://countriesnow.space/api/v0.1/countries'

class Search_combobox(widgets.QComboBox):
    def __init__(self, parent, search, width):
        super().__init__(parent)
        self.setEditable(True)
        self.search = search
        self.cities = []
        #focus
        self.setFocusPolicy(core.Qt.FocusPolicy.NoFocus)
        self.lineEdit().setFocusPolicy(core.Qt.FocusPolicy.NoFocus)
        self.view().setFocusPolicy(core.Qt.FocusPolicy.NoFocus) 
        #styles
        
        self.setStyleSheet("""
    /* Само поле ввода */
    QComboBox {
        background-color: rgba(0, 0, 0, 60);
        border: 2px solid white;
        border-radius: 10px;
        color: white;
        font-size: 16px;
        padding: 5px;
    }
    
    /* Выпадающий список */
    QComboBox QAbstractItemView {
        background-color: rgba(0, 0, 0, 200);
        border: 1px solid white;
        border-radius: 5px;
        color: white;
        selection-background-color: rgba(255, 255, 255, 50);
    }
""")
        self.setFixedWidth(width)
        # Загружаем данные ОДИН РАЗ при создании
        response = requests.get(url)
        self.data_dict = response.json()
        
        with open("static/json/citys_data.json", mode="w", encoding='utf-8') as file:
            json.dump(obj=self.data_dict, fp=file, indent=4, ensure_ascii=False)

        # Загружаем города ОДИН РАЗ
        self.load_cities()
        
        # Подключаем фильтрацию к вводу текста
        self.search.textChanged.connect(self.filter_cities)

    def load_cities(self):
        # Загружаем все города один раз
        for country in self.data_dict['data']:
            for city in country['cities']:
                self.cities.append(city)
        
        self.cities = sorted(self.cities)
        # self.addItems(self.cities)
        
        # Настраиваем completer
        completer = widgets.QCompleter(self.cities)
        # completer.setCaseSensitivity(core.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(core.Qt.MatchFlag.MatchStartsWith)
        self.setCompleter(completer)
        self.activated.connect(self.clicked)

    def clicked(self, index):
        city = self.itemText(index)
        self.search.setText(str(city))

    def filter_cities(self, text):
        # Очищаем и фильтруем при каждом вводе
        self.clear()
        
        if text == "":
            self.clear()
        else:
            filtered = []
            
            for city in self.cities:          # перебираем все города
                if city.lower().startswith(   # если город начинается с...
                    text.lower()              # ...введённого текста (оба в нижнем регистре)
                ):
                    filtered.append(city) # добавляем в список
                    
            self.addItems(filtered[:15])
            # self.showPopup()
