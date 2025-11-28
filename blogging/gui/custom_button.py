

from PyQt6.QtWidgets import (QPushButton)
from PyQt6.QtGui import  QCursor
from PyQt6.QtCore import Qt
class CustomButton(QPushButton):

    def __init__(self, text) -> None:
        
        super().__init__(text=text)
        
        self.pointing_cursor = QCursor(Qt.CursorShape.PointingHandCursor)
        self.setCursor(self.pointing_cursor)



    