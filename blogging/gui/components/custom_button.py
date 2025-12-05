

from PyQt6.QtWidgets import (QPushButton)
from PyQt6.QtGui import  QCursor, QColor
from PyQt6.QtCore import Qt
from blogging.gui.components.utils import createShadow 
class CustomButton(QPushButton):

    def __init__(self, text) -> None:
        
        super().__init__(text=text)
        
        self.pointing_cursor = QCursor(Qt.CursorShape.PointingHandCursor)
        self.setCursor(self.pointing_cursor)
        self.setGraphicsEffect(createShadow(0, 10, 5, QColor(0,0,0,50)))



    