from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
  
    QDialog,
    QLineEdit,
    QGridLayout,
    QPlainTextEdit,
    QTextEdit,
)

from PyQt6.QtCore import Qt

from blogging.gui.components.custom_button import CustomButton

from blogging.gui.components.utils import newQFrame
from blogging.controller import Controller

from blogging.gui.components.handle_error import ErrorGUI


class PostsPage:
    def __init__(self, controller: Controller):
        self.controller = controller

        self.plain_text_edit = QPlainTextEdit()
      
     
        self.plain_text_edit.setFixedHeight(400)
        self.plain_text_edit.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )  
        self.plain_text_edit.setReadOnly(True)

      
        self.page_grid = newQFrame(QGridLayout(), id="button-grid")
        self.page_layout = self.page_grid.layout()
        self.run_ui()

    """
    run_ui will have same button screen or similar as to blogs-page
    add update delete, searchbar is the same so no changes there, list_posts ig is a dialog
    BUT it will toggle after every search. 
    have the page show current blog name and its actions
    
    """

    def handle_text_edit(self, *args, post=None):

        code_input, title, text, btn, subbtn = args

        if post:
            title.setEnabled(True)
            text.setEnabled(True)

        else:
            title.setEnabled(False)
            text.setEnabled(False)

    def handle_search(self, *args):

        code_input, title, text, btn, subbtn = args
        if not code_input.text().isdigit():
            return 
        self.search_id = int(code_input.text())

        post = self.controller.search_post(self.search_id)
        if post:
            self.handle_text_edit(*args, post=post)
            title.setText(post.title)
            text.setPlainText(post.text)
            code_input.setEnabled(False)
            btn.setEnabled(True)
           

        else:
            ErrorGUI(
                self.dialog,
                "Oops",
                error_msg="Can't Update Post that doesn't Exists",
            )
            code_input.setText("")

    def handle_btn_edit(self, *args):
        code_input, title, text, btn, subbtn = args

        if title.text() and len(text.toPlainText()) > 1:

            btn.setEnabled(True)
        else:
            btn.setEnabled(False)

   

  

    def display_posts(self, posts=None):
        self.plain_text_edit.setPlainText("")
        if not posts:
            posts = self.controller.list_posts()
        try:
            for post in posts:
                title_text = f"""
                [title]
                {post.title}
                """
                text_layout = f"""
                [text]
                {post.text}
                
                """
                self.plain_text_edit.appendPlainText(
                    f"[Post Code: {post.code}] \n{title_text} {text_layout}"
                )
                
        except Exception as e:
            ErrorGUI(
                parent=self.plain_text_edit,
                title="Uhm...",
                error_msg="Something went wrong displaying posts"
            )

    def post_modal(self, innerText):
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

        # Code input
        code_input = QLineEdit()
        code_input.setPlaceholderText("Post Code")

        post = None

        # Name

        title_input = QLineEdit(post.title if post else None)
        title_input.setPlaceholderText("Post Title")
        # Email

        text_input = QTextEdit(post.text if post else None)
        text_input.setPlaceholderText("Post Text")

        submit_btn = CustomButton(text=f"{innerText}")
        submit_btn.setEnabled(False)
        search_btn = CustomButton(text=f"Search")
        search_btn.setObjectName("search-btn-modal")

        form_list = [
            code_input,
            title_input,
            text_input,
            submit_btn,
            search_btn,
        ]

        if "Update" in innerText or "Delete" in innerText:
            title_input.setEnabled(False)
            
            text_input.setEnabled(False)
        else:
            code_input.hide()

        [
            item.textChanged.connect(lambda: self.handle_btn_edit(*form_list))
            for item in form_list
            if isinstance(item, QLineEdit) or isinstance(item, QTextEdit)
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
            code_input.text() if code_input.text() else "",
            title_input.text(),
            text_input.toPlainText(),
            close
        ]

    def run_ui(self):

        posts_header = QLabel("Posts")

        posts_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.page_layout.addWidget(posts_header, 0,0,1,3)  # type: ignore

        self.page_layout.addWidget(self.plain_text_edit, 1, 0, 1, 3)
        
        add_btn = CustomButton(text="Add Posts")

        update_btn = CustomButton(text="Update Posts")
        delete_btn = CustomButton(text="Delete Posts")

        add_btn.clicked.connect(lambda: self.handle_add_post())
        update_btn.clicked.connect(lambda: self.handle_update_post())
        delete_btn.clicked.connect(lambda: self.handle_delete_post())



        buttons_list = [add_btn, update_btn, delete_btn]
        fbf_grid = [(2, 0), (2, 1), (2, 2)]

        for i in range(0, len(buttons_list)):
            self.page_layout.addWidget(
                buttons_list[i], fbf_grid[i][0], fbf_grid[i][1]
            )

    def handle_add_post(self):
        """
        Add post GUI logic 
        """
        form_data = self.post_modal("Add")

        code, title, text, close = form_data
        if close:
            try:
                self.controller.create_post(title=title, text=text)
                self.display_posts()
            except Exception as e:
                ErrorGUI(
                    self.dialog,
                    "Oops",
                    error_msg="Something went wrong",
                )

    def handle_update_post(self):
        """
        Code to update the modal, checks the close variable
        """
        form_data = self.post_modal("Update")
        code, title, text, close = form_data
        if close:
            try:
                self.controller.update_post(title=title, text=text, code=int(code))
                self.display_posts()
            except Exception as e:
                ErrorGUI(
                    self.dialog,
                    "Oops",
                    error_msg="Something went wrong",
                )

    def handle_delete_post(self):

        """
        delete GUI logic 
        """
        form_data = self.post_modal("Delete")
        code = form_data[0]
        close = form_data[3]
        if close:
            try:
                self.controller.delete_post(code=int(code))
                self.display_posts()
            except Exception as e:
                ErrorGUI(
                    self.dialog,
                    "Oops",
                    error_msg="Something went wrong",
                )
