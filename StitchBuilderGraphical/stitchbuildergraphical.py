# This Python file uses the following encoding: utf-8
import sys

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from UnicodeSymbols import UnicodeSymbols

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_StitchBuilderGraphical

GRID_COLUMN_COUNT = 6

class StitchBuilderGraphical(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.ui = Ui_StitchBuilderGraphical()
    self.ui.setupUi(self)
    self.setLayout(self.ui.verticalLayout)

    self.symbolmap = UnicodeSymbols()
    for i, char in enumerate(self.symbolmap.chars_light):
      twidget = self.createCharLabel(char)
      self.ui.symbolGridLight.addWidget(twidget, i / GRID_COLUMN_COUNT, i % GRID_COLUMN_COUNT, QtCore.Qt.AlignCenter)
    for i, char in enumerate(self.symbolmap.chars_med):
      twidget = self.createCharLabel(char)
      self.ui.symbolGridMedium.addWidget(twidget, i / GRID_COLUMN_COUNT, i % GRID_COLUMN_COUNT, QtCore.Qt.AlignCenter)
    for i, char in enumerate(self.symbolmap.chars_dark):
      twidget = self.createCharLabel(char)
      self.ui.symbolGridDark.addWidget(twidget, i / GRID_COLUMN_COUNT, i % GRID_COLUMN_COUNT, QtCore.Qt.AlignCenter)

  def createCharLabel(self, character):
      font_size = 18
      labeltext = "<html><head/><body><p align=\"center\"><span style=\" font-size:{0}pt;\">{1}</span></p></body></html>".format(font_size, character)
      twidget = QLabel(character,alignment=QtCore.Qt.AlignCenter)
      twidget.setText(labeltext)
      return twidget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = StitchBuilderGraphical()
    widget.show()
    sys.exit(app.exec())
