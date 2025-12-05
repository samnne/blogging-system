
from PyQt6.QtWidgets import QFrame, QGraphicsDropShadowEffect
from PyQt6.QtGui import QIntValidator
def newQFrame(layout, id):
    qframe = QFrame()

    qframe.setObjectName(id)
    qframe.setLayout(layout)

    return qframe

def createShadow(xoff, yoff, r, color):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(r)
        shadow.setXOffset(xoff)
        shadow.setYOffset(yoff)
        shadow.setColor(color)

        return shadow

int_input_validator = QIntValidator(bottom=0, top=2147483647)
