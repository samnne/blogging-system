import sys
from blogging.configuration import Configuration
from blogging.controller import Controller
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QLabel,
    QFrame,
    QLineEdit,
    QPushButton,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtGui import QPixmap, QColor, QCursor
from blogging.gui.dashboard import Dashboard
from blogging.gui.components.handle_error import ErrorGUI


class BloggingGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # set autosave to True to ensure persistence is working
        self.configuration = Configuration()
        self.configuration.__class__.autosave = True
        # Continue here with your code!

       
        self.controller = Controller()

        self.setWindowTitle("uBlog")

        with open("blogging/gui/login.css", "r") as f:
            self.setStyleSheet(f.read())

        self.setMaximumSize(1200, 720)
        self.setMinimumSize(800, 600)

        self.pointing_cursor = QCursor(Qt.CursorShape.PointingHandCursor)

        self.loginUI()

    def openDashboard(self):
        self.dashboard = Dashboard(self.controller, self)

        self.close()

    def createShadow(self, xoff, yoff, r, color):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(r)
        shadow.setXOffset(xoff)
        shadow.setYOffset(yoff)
        shadow.setColor(color)

        return shadow

    def submitForm(self, user_input: QLineEdit, pass_input: QLineEdit):
        user_text = user_input.text()
        pass_text = pass_input.text()

        try:
            
            logged_in = self.controller.login(user_text, pass_text)

            if logged_in:
                user_input.setText("")
                pass_input.setText("")
                self.openDashboard()
        except:
            ErrorGUI(self, 
                "Bad Login Credentials",
                "Incorrect Username or Password"
                )
            

    def loginUI(self):
        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        hbox = QHBoxLayout()

        form_side = QFrame()

        form_layout = QVBoxLayout()
        form_layout.setSpacing(12)
        form_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_side.setFixedSize(400, 500)
        
        form_layout.setContentsMargins(50, 20, 50, 20)
        form_side.setLayout(form_layout)

        shadow = self.createShadow(0, 12, 40, Qt.GlobalColor.black)

        form_side.setGraphicsEffect(shadow)

        hbox.addWidget(form_side, 1)

        logo = QLabel()
        pix = QPixmap("blogging/gui/images/logo.png")
        logo.setPixmap(pix)
        logo.setObjectName("logo-header")

        form_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        login = QLabel("Login")
        login.setObjectName("login-header")
        login.setStyleSheet("font-size: 32px; font-weight: bold;")

        form_layout.addWidget(login, alignment=Qt.AlignmentFlag.AlignCenter)

        # The form itself
        form = QVBoxLayout()

        form.setSpacing(12)

        username = QLineEdit()
        user_label = QLabel("Username")
        user_label.setStyleSheet("font-size:16px; font-weight:bold; color: #000")

        username.setPlaceholderText("Username")
       # type: ignore
        username.setObjectName("username")
        u_shadow = self.createShadow(0, 4, 6, QColor(0, 0, 0, 20))

        username.setGraphicsEffect(u_shadow)

        pass_label = QLabel("Password")
        pass_label.setStyleSheet("font-size:16px; font-weight:bold; color: #000")

        password = QLineEdit()
        password.setPlaceholderText("Password")
        password.setObjectName("password")
        p_shadow = self.createShadow(0, 4, 6, QColor(0, 0, 0, 20))

        password.setGraphicsEffect(p_shadow)
        password.setEchoMode(QLineEdit.EchoMode.Password)

        form.addWidget(user_label)
        form.addWidget(username)
        form.addWidget(pass_label)
        form.addWidget(password)

        form_layout.addLayout(form)

        # buttons on the bottom
        buttons = QHBoxLayout()

        login_btn = QPushButton("Login")
        login_btn.setObjectName("accentButton")
        login_btn.setCursor(self.pointing_cursor)
        login_btn.clicked.connect(lambda: self.submitForm(username, password))

        quit_btn = QPushButton("Quit")
        quit_btn.setCursor(self.pointing_cursor)
        quit_btn.clicked.connect(lambda: self.close())
        buttons.addWidget(login_btn)
        buttons.addWidget(quit_btn)

        form_layout.addLayout(buttons)
        form_layout.insertStretch(0, 1)
        form_layout.addStretch(1)

        central_widget.setLayout(hbox)


"""
Colors To Use: Move this to stylesheet later

Gold color for text #fca311

"""


def main():
    app = QApplication(sys.argv)
    window = BloggingGUI()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
