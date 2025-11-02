from datetime import datetime as Datetime


class Post:
    def __init__(self, code: int, title: str, text: str, creation: Datetime, update: Datetime):
        self.code = code
        self.title = title
        self.text = text
        self.creation = creation
        self.update = update
