from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,

    QSizePolicy,
    QHeaderView,
    QHBoxLayout,
    QDialog,
    QLineEdit,
)
from PyQt6.QtGui import QIntValidator

from PyQt6.QtCore import Qt
from blogging.gui.components.table_view import TableModel
from blogging.gui.components.custom_button import CustomButton
from blogging.helper import convert_data
from blogging.gui.components.utils import newQFrame
from blogging.controller import Controller

from blogging.gui.components.handle_error import ErrorGUI
from blogging.gui.components.utils import int_input_validator


class BlogsPage:

    def __init__(
        self, blogs_table, table_list_data, table_header, controller: Controller
    ):
        # Blogs Page

        self.table_list_data = table_list_data
        self.controller = controller
        self.table_header = table_header
        self.blogs_table = blogs_table
        self.blogs_page = newQFrame(QVBoxLayout(), id="page")
        self.bpl = self.blogs_page.layout()
        self.run_ui()

    def show(self):
        self.blogs_page.show()
    def hide(self):
        self.blogs_page.close()
    def run_ui(self):
       
        # Blogs page parent layout
        

        # The Blog System Header
        blogs_header = QLabel("Blogs")

        blogs_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.bpl.addWidget(blogs_header, stretch=1)  # type: ignore

        # Main content that holds the table
        blogs_page_main = newQFrame(QVBoxLayout(), id="main-menu")
        blog_page_main_l = blogs_page_main.layout()
        blogs_page_main.setContentsMargins(10, 10, 10, 10)
        # The blog table

        self.blogs_table_model = TableModel(
            convert_data(data=self.table_list_data), self.table_header
        )

        self.blogs_table.setShowGrid(False)
        self.blogs_table.setAlternatingRowColors(True)
        self.blogs_table.setModel(self.blogs_table_model)

        blog_page_main_l.addWidget(self.blogs_table)

        # Set table styling
        self.blogs_table.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        header = self.blogs_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.blogs_table.verticalHeader().setDefaultSectionSize(55)
        self.blogs_table.verticalHeader().setVisible(False)
        self.bpl.addWidget(blogs_page_main, stretch=5)  # type: ignore

        add_blog = CustomButton("Add Blog")
        add_blog.clicked.connect(self.handle_add_blog)
        update_blog = CustomButton("Update Blog")
        update_blog.clicked.connect(self.handle_update_blog)
        delete_blog = CustomButton("Delete Blog")
        delete_blog.clicked.connect(self.handle_delete_blog)

        self.modifier_buttons = newQFrame(QHBoxLayout(), id="buttons")
        self.modifier_buttons_l = self.modifier_buttons.layout()
        mb_list = [add_blog, update_blog, delete_blog]

        [self.modifier_buttons_l.addWidget(widget) for widget in mb_list]

        blog_page_main_l.addWidget(self.modifier_buttons)
        self.bpl.addWidget(blogs_page_main, stretch=5)  # type: ignore

    def find_row_by_id(self, blog_id):
        """
        Ensures the correct row is removed when deleting.
        """
        for row in range(self.blogs_table_model.rowCount()):
            idx = self.blogs_table_model.index(row, 0)
            if idx.data() == blog_id:
                return row
        return -1

    def blog_modal(self, innerText):
        """
        The blog modal
        """
        self.dialog = QDialog()

        self.dialog.setStyleSheet(
            """
            QWidget {
                background: white;
                color: black;
            }
            QLabel{
                font-weight: bold;
                font-size: 32px;
                padding: 20px;
                
            }
            QFrame QPushButton{
                background: #e63946;
                padding: 8px;
                border-radius: 12px;
                color: white;
            }
            QFrame QPushButton:hover{
                background: #e6394690;
                
            }
            QFrame QPushButton:disabled{
                background: #dbb4b7;
                
            }
            
            QFrame QLineEdit{
                border: 1px solid rgba(0, 0, 0, 0.2);
                padding: 8px;
                border-radius: 12px;
            }
            QFrame QLineEdit:disabled{
                border:none;
                background: rgba(0,0,0,0.2);
                padding: 8px;
                border-radius: 12px;
            }
            #search-btn-modal{
                background: #457b9d;
            }
            #search-btn-modal:hover{
                background: #457b9dee;
            }
            """
        )

        layout = QVBoxLayout()
        # Form
        form = newQFrame(QVBoxLayout(), id="form-modal")

        form.setFixedWidth(300)

        form_layout = form.layout()

        # Form header
        header = QLabel("Add New Blog" if "Add" in innerText else innerText)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(header)
        # Id

        blog = None

        id_input = QLineEdit(blog.id if blog else None)

        id_input.setPlaceholderText("Blog ID")
        id_input.setValidator(int_input_validator)

        # Name

        name_input = QLineEdit(blog.name if blog else None)
        name_input.setPlaceholderText("Blog Name")
        # Email

        email_input = QLineEdit(blog.email if blog else None)
        email_input.setPlaceholderText("Blog Email")

        # URL

        url_input = QLineEdit(blog.url if blog else None)
        url_input.setPlaceholderText("Blog URL")

        submit_btn = CustomButton(text=f"{innerText}")
        submit_btn.setEnabled(False)
        search_btn = CustomButton(text=f"Search")
        search_btn.setObjectName("search-btn-modal")

        form_list = [
            id_input,
            name_input,
            email_input,
            url_input,
            submit_btn,
            search_btn,
        ]

        if "Update" in innerText or "Delete" in innerText:
            name_input.setEnabled(False)
            email_input.setEnabled(False)
            url_input.setEnabled(False)

        [
            item.textChanged.connect(lambda: self.handle_btn_edit(*form_list))
            for item in form_list
            if isinstance(item, QLineEdit)
        ]

        for widget in form_list:
            if widget != search_btn:
                form_layout.addWidget(widget)
            elif (
                widget == search_btn and "Update" in innerText or "Delete" in innerText
            ):
                form_layout.addWidget(widget)

        search_btn.clicked.connect(lambda: self.handle_search(*form_list))

        submit_btn.clicked.connect(lambda: self.dialog.accept())

        layout.addWidget(form)

        self.dialog.setLayout(layout)

        close = self.dialog.exec()

        return [
            int(id_input.text()) if id_input.text().isdigit() else "",
            name_input.text(),
            email_input.text(),
            url_input.text(),
            close
        ]

    def handle_btn_edit(self, *args):
        """
        Enables/Disables the sumbit button in the form
        """
        id_input, name_input, email_input, url_input, btn, sbtn = args
        if not id_input.text():
            sbtn.setEnabled(True)

        if (
            id_input.text()
            and name_input.text()
            and email_input.text()
            and url_input.text()
        ):

            btn.setEnabled(True)
        else:
            btn.setEnabled(False)

    def handle_search(self, *args):
        id_input, name_input, email_input, url_input, btn, sbtn = args
        if not id_input.text().isdigit():
            return 
        self.search_id = int(id_input.text())

        blog = self.controller.search_blog(self.search_id)
        if blog:
            self.handle_text_edit(name_input, email_input, url_input, blog=blog)
            name_input.setText(blog.name)
            email_input.setText(blog.email)
            url_input.setText(blog.url)

            sbtn.setEnabled(False)

        else:
            ErrorGUI(
                self.dialog,
                "Oops",
                error_msg="Can't Update Blog that doesn't Exists",
            )
            id_input.setText("")
            pass

    def handle_add_blog(self):

        form_data = self.blog_modal(innerText="Add Blog")

        blog_id, name, email, url, close = form_data
        if close:
            try:
                self.controller.create_blog(id=blog_id, name=name, url=url, email=email)
                self.blogs_table_model.add_row(form_data)
            except Exception as e:
                ErrorGUI(
                    self.dialog,
                    "Oops",
                    error_msg="Blog already exists",
                )

    def delete_blog(self, form_data, dialog):
        
        blog_id, name, email, url, close = form_data
        if close:
            try:
                self.controller.delete_blog(id=blog_id)
                self.blogs_table_model._data.pop(self.find_row_by_id(blog_id=blog_id))
                self.blogs_table_model.layoutChanged.emit()

            except Exception as e:
                ErrorGUI(
                    self.dialog,
                    "Oops",
                    error_msg="Can't Delete Current Blog",
                )
        dialog.close()


    def handle_delete_blog(self):
        form_data = self.blog_modal("Delete")
        if not form_data[4]: # the close variable to detemine whether to run dialog GUI
            return
        confirm = QDialog()
        confirm.setStyleSheet("""
             QWidget {
                background: white;
                color: black;
            }
            QLabel{
                font-weight: bold;
                font-size: 18px;
                padding: 20px;
            }
            QFrame QPushButton{
                background: #e63946;
                padding: 8px;
                border-radius: 12px;
                color: white;
            }
            QFrame QPushButton:hover{
                background: #e6394690;
                
            }
        """
        )
        confirm.setWindowTitle("Are You Sure?")
        conf_layout = QVBoxLayout()
        confirm.setLayout(conf_layout)

        label = QLabel(
            "Are you sure you want to delete this blog? \nThis action cannot be undone."
        )
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cancel_button = CustomButton("Cancel")
        cancel_button.setStyleSheet(
            """
            QPushButton{
                background:  rgba(0,0,0,0.5);
            }
            QPushButton:hover{
                background:  rgba(0,0,0,0.2);
            }
            """
        )
        
        confirm_delete = CustomButton("Delete")
        confirm_delete.clicked.connect(lambda: self.delete_blog(form_data, confirm))
        conf_layout.addWidget(label)
        cancel_button.clicked.connect(lambda: confirm.accept())

        button_frame = newQFrame(QHBoxLayout(), id="buttons")
        button_frame.setContentsMargins(20, 20, 20, 20)
        button_layout = button_frame.layout()
        button_layout.addWidget(confirm_delete)

        button_layout.addWidget(cancel_button)

        
        conf_layout.addWidget(button_frame)
        if form_data[0]:

            confirm.exec()
        
        


    def handle_text_edit(self, *args, blog=None):
        """
        Disables/Enables the LineEdits
        """
        name_input, email_input, url_input = args

        if blog:
            name_input.setEnabled(True)
            email_input.setEnabled(True)
            url_input.setEnabled(True)
        else:
            name_input.setEnabled(False)
            email_input.setEnabled(False)
            url_input.setEnabled(False)

    def handle_update_blog(self):

        form_data = self.blog_modal(innerText="Update Blog")
        blog_id, name, email, url, close = form_data
        if close:
            try:
                self.controller.update_blog(
                    search_id=self.search_id,
                    new_id=blog_id,
                    name=name,
                    url=url,
                    email=email,
                )
                self.blogs_table_model._data[self.find_row_by_id(self.search_id)] = (
                    form_data
                )
                self.blogs_table_model.layoutChanged.emit()
            except Exception as e:
                ErrorGUI(
                    self.dialog,
                    "Oops",
                    error_msg="Can't Update Current Blog",
                )

    def returnFrame(self):
        return self.blogs_page
