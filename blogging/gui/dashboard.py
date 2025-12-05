import sys
from blogging.configuration import Configuration

from blogging.gui.pages.blogs_page import BlogsPage
from blogging.gui.pages.posts_page import PostsPage
from blogging.gui.components.custom_button import CustomButton
from blogging.gui.components.table_view import TableModel
from blogging.controller import Controller


from PyQt6.QtCore import Qt
from blogging.helper import convert_data
from blogging.gui.components.utils import newQFrame, createShadow
from blogging.gui.components.handle_error import ErrorGUI
from blogging.gui.components.utils import int_input_validator

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QHeaderView,
    QWidget,
    QLabel,
    QFrame,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QGraphicsDropShadowEffect,
    QTableView,
    QSizePolicy,
    QDialog,
    QAbstractItemView,
)
from PyQt6.QtGui import QPixmap, QColor, QCursor, QFont, QIntValidator


class Dashboard(QMainWindow):

    def __init__(self, controller: Controller, login_window, current_user: str) -> None:
        super().__init__()
        self.setWindowTitle("uBlog Dashboard")
        self.setMinimumSize(1200, 720)
        with open("blogging/gui/dashboard.css", "r") as f:
            self.setStyleSheet(f.read())
        self.current_user = current_user
        self.controller = controller
        self.login_winodw = login_window
        self.blog_table_header = ["Id", "Name", "Email", "URL"]
        
        self.table_list_data = self.controller.list_blogs()
        self.blogs_table = QTableView()
        self.posts_page = PostsPage(controller=self.controller)
        self.blogs_page_main = BlogsPage(
            blogs_table=self.blogs_table,
            controller=self.controller,
            table_header=self.blog_table_header,
            table_list_data=self.table_list_data,
        )

        self.main_layout()

        self.show()

    # Helper function in development -> TODO: Comment Out
    def update_css(self, css_file_path):
        with open(css_file_path, "r") as f:
            self.setStyleSheet(f.read())

    def handle_logout(self):
        # Logout of the system and return to main screen
        self.controller.logout()

        self.login_winodw.show()
        self.close()

    def logout_ui(self):
        """
        The Logout divider in the top navigation bar
        """
        logout = newQFrame(layout=QHBoxLayout(), id="logout-btn")
        logout_btn = CustomButton("Logout ➜]")
        logout_btn.setFixedWidth(100)

        logout_btn.clicked.connect(lambda: self.handle_logout())

        logout_l = logout.layout()
        current_user_label = QLabel(f"Current User:  {self.current_user.capitalize()}")
        current_user_label.setStyleSheet(
            """
            QLabel {
                color: #457b9d;
               
            }
            """
        )
        logout_l.addWidget(current_user_label)
        logout_l.setContentsMargins(250, 10, 0, 10)  # type: ignore
        logout_l.addWidget(logout_btn, stretch=1)  # type: ignore
        return logout

    def handle_search(self, searchbar_input, searchbar_submit):
        """
        Handles the top navigation search bar feature.
        """

        if self.controller.get_current_blog() and searchbar_input.text().isdigit():
            post = self.controller.search_post(int(searchbar_input.text()))
            if post:

                self.posts_page.display_posts([post])
        elif self.controller.get_current_blog() and self.searchbar_input.text():
            posts = self.controller.retrieve_posts(searchbar_input.text())
            if posts:
                self.posts_page.display_posts(posts)
        elif searchbar_input.text().isdigit():
            blog = self.controller.search_blog(int(searchbar_input.text()))
            if blog:
                new_model = TableModel(
                    data=[blog.to_list()], headers=self.blog_table_header
                )
                self.blogs_table.setModel(new_model)

        elif searchbar_input.text():
            blogs = self.controller.retrieve_blogs(search_string=searchbar_input.text())

            new_model = TableModel(
                data=convert_data(blogs), headers=self.blog_table_header
            )
            self.blogs_table.setModel(new_model)

    def handle_search_button(self, input_text, btn):
        if not input_text.text():
            # dialog
            btn.setEnabled(False)
            self.blogs_table.setModel(self.blogs_page_main.blogs_table_model)
            if self.controller.get_current_blog():
                self.posts_page.display_posts()
        else:
            btn.setEnabled(True)

    def search_bar(self):
        searchbar = newQFrame(QHBoxLayout(), id="searchbar")
        sbl = searchbar.layout()  # type: ignore
        self.searchbar_input = QLineEdit()
        self.searchbar_input.setGraphicsEffect(
            createShadow(0, 10, 5, QColor(0, 0, 0, 80))
        )
        self.searchbar_input.textChanged.connect(
            lambda: self.handle_search_button(self.searchbar_input, searchbar_submit)
        )
        self.searchbar_input.setPlaceholderText("Blogs")
        searchbar_submit = CustomButton("Search")
        searchbar_submit.clicked.connect(
            lambda: self.handle_search(
                searchbar_input=self.searchbar_input, searchbar_submit=searchbar_submit
            )
        )

        searchbar_submit.setEnabled(False)

        sbl.addWidget(self.searchbar_input, stretch=2)  # type: ignore
        sbl.addWidget(searchbar_submit, stretch=1)  # type: ignore
        sbl.setContentsMargins(50, 10, 50, 10)  # type:ignore

        return searchbar

    def handle_unset_blog(self):
        self.controller.unset_current_blog()
        self.current_blog_label.setText("Current Blog: None")
        self.searchbar_input.setPlaceholderText("Blogs")
        self.show_blogs_page()

    def handle_set_blog(self, dialog):
        if not self.blog_id_input.text():
            return
        if self.controller.get_current_blog():
            QMessageBox.warning(
                dialog,
                "Hold It!",
                "Current blog already set",
                QMessageBox.StandardButton.Ok,
            )
            return
        elif not self.controller.search_blog(int(self.blog_id_input.text())):
            QMessageBox.warning(
                dialog,
                "Hold It!",
                "Blog Doesn't Exist",
                QMessageBox.StandardButton.Ok,
            )
            return
        else:

            self.controller.set_current_blog(int(self.blog_id_input.text()))
            self.current_blog_label.setText(
                f"Current Blog: {self.controller.get_current_blog().name}"  # type: ignore
            )
            self.searchbar_input.setPlaceholderText("Posts")
            self.show_posts_page()
            dialog.close()

    def show_blogs_page(self):
        self.blogs_page_main.show()
        self.searchbar_input.setPlaceholderText("Blogs")
        self.posts_page.page_grid.hide()

    def show_posts_page(self):

        self.blogs_page_main.hide()
        self.searchbar_input.setPlaceholderText("Posts")
        self.posts_page.page_grid.show()
        self.posts_page.display_posts()

    def set_current_blog_ui(self):
        if self.controller.get_current_blog():
            self.show_posts_page()
            return
        dialog = QDialog()
        dialog.setStyleSheet(
            """
            QDialog {
                padding: 20px;
                color: black;

                background: #f4f1de;
            }
            QLabel{
                font-size: 24px;
                font-weight: bold;
                color: black;
            }
            QDialog QLineEdit {
                background: #f4f1de;
                padding: 8px;
                font-weight: bold;
                color: black;
            }
            QDialog QPushButton{
                background: #457b9d;
                color: white;
                font-weight: bold;
                padding: 4px; 
            }
            """
        )

        dl = QVBoxLayout()

        label = QLabel("Please Set Current Blog")
        self.blog_id_input = QLineEdit()
        self.blog_id_input.setPlaceholderText("Blog Id")
        self.blog_id_input.setValidator(int_input_validator)
        dl.addWidget(label)
        dl.addWidget(self.blog_id_input)

        dialog.setLayout(dl)
        btn = CustomButton("Set Blog")

        btn.clicked.connect(lambda: self.handle_set_blog(dialog))

        dl.addWidget(btn)
        dialog.exec()

    def main_layout(self):
        """
        The main gui layout of this current window

        Note: Variable names ending in *_l _l: layout,
        for example, blogs_page_l => is read as blogs page layout
        """
        center_widget = QWidget()
        self.setCentralWidget(center_widget)

        hbox = QVBoxLayout()

        # Top Nav
        top_nav = newQFrame(QHBoxLayout(), id="top-nav")
        tnl = top_nav.layout()
        logo = newQFrame(QHBoxLayout(), id="logo")
        logo.setFixedHeight(100)

        searchbar = self.search_bar()

        logout = self.logout_ui()

        tn_list = [logo, searchbar, logout]

        [tnl.addWidget(item, stretch=1) for item in tn_list]  # type: ignore

        # Main Content -> PAGE dependent...
        content = newQFrame(QHBoxLayout(), id="content")

        # Side Nav with Blog and Posts search?
        # at the bottom put current user data? or current blog id and name?
        aside = newQFrame(QVBoxLayout(), id="aside")
        al = aside.layout()

        # top layout to display 2 buttons
        # Blogs, Posts
        a_top = newQFrame(QVBoxLayout(), id="aside-t")
        a_top_l = a_top.layout()
        a_top_l.setAlignment(Qt.AlignmentFlag.AlignTop)  # type: ignore
        a_top_blogs = CustomButton("Blogs")

        a_top_blogs.clicked.connect(lambda: self.show_blogs_page())
        a_top_blogs.setFixedHeight(50)

        a_top_posts = CustomButton("View Current Blog")
        a_top_posts.setStyleSheet(
            """
            QPushButton {                
                background: #457b9d; 
                color: white;

            }
            QPushButton:hover {
                background: #457b9dd8;
            }
            """
        )

        a_top_posts.clicked.connect(lambda: self.set_current_blog_ui())
        a_top_posts.setFixedHeight(50)

        a_top_l.addWidget(a_top_blogs)  # type:ignore
        a_top_l.addWidget(a_top_posts)  # type:ignore
        # label and pushbutton to set current blog
        a_bottom = newQFrame(QHBoxLayout(), id="aside-b")

        a_b_l = a_bottom.layout()
        self.current_blog_label = CustomButton("Current Blog: None")
        self.current_blog_label.setStyleSheet(
            """
            QPushButton{
                padding: 10px;
                background: #f4f1de;
                color: #457b9d;
                font-size: 20px;
                font-weight: bold;

            }
            QPushButton:hover{
                background: #a8dadc;
            }
        """
        )
        self.current_blog_label.setGraphicsEffect(None)

        self.current_blog_label.clicked.connect(self.handle_unset_blog)
        a_b_l.addWidget(self.current_blog_label)  # type: ignore

        al.addWidget(a_top, stretch=3)  # type: ignore
        al.addWidget(a_bottom, stretch=1)  # type: ignore

        cl = content.layout()
        cl.addWidget(aside, stretch=1)  # type: ignore
        cl.addWidget(self.blogs_page_main.returnFrame(), stretch=3)  # type: ignore
        self.posts_page.page_grid.hide()
        cl.addWidget(self.posts_page.page_grid, stretch=3)  # type: ignore
        cl.setSpacing(0)  # type: ignore

        hbox.addWidget(top_nav, stretch=1)
        hbox.addWidget(content, stretch=6)

        # button = CustomButton("")
        # button.clicked.connect(lambda: self.update_css("blogging/gui/dashboard.css"))
        # hbox.addWidget(button)

        center_widget.setLayout(hbox)


def main():
    app = QApplication(sys.argv)
    con = Controller()
    con.login("user", "123456")
    window = Dashboard(con, None, "")
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
