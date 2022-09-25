# This Python file uses the following encoding: utf-8
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QImage


class ImageLabel(QLabel):
    def __init__(self, parent=None):
      super().__init__(parent)
      self.img = None
      self.targetSize = self.size()

    def setImage(self, img):
      """
      Expects a QImage
      """
      self.img = img.convertToFormat(QImage.Format_RGB32)
      self.resizeImage()#will force a repaint

    def resizeImage(self):
      if self.img is None:
        return
      pixmap = QPixmap(self.img).scaled(self.targetSize, Qt.KeepAspectRatio)
      self.setPixmap(pixmap)

    def resizeEvent(self, evt):
      super().resizeEvent(evt)
      self.targetSize = evt.size()
      self.resizeImage()

