
from PyQt6.QtWidgets import QFrame

def newQFrame(layout, id):
    qframe = QFrame()

    qframe.setObjectName(id)
    qframe.setLayout(layout)

    return qframe
