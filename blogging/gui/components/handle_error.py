
from PyQt6.QtWidgets import (
    QMessageBox
)


class ErrorGUI(QMessageBox):
    def __init__(self, parent, title, error_msg):
        super().__init__()
        
        self.warning(parent, title, error_msg, QMessageBox.StandardButton.Ok)

        