import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
from PyQt6.QtGui import QFontDatabase, QFont

import sys

widgets.QApplication.setAttribute(core.Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

app_obj = widgets.QApplication(sys.argv)
font_id = QFontDatabase.addApplicationFont("fonts/Nunito-Regular.ttf")
app_obj.setStyleSheet("QLabel, QComboBox, QRadioButton  { color: white; }")



if font_id == -1:
    print("❌ шрифт не загрузился")
else:
    family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app_obj.setFont(QFont(family, 11))