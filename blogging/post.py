from datetime import datetime 


class Post:
    def __init__(self, code: int, title: str, text: str):
        # auto incremented key / unique ID
        self.code = code
        
        # Post data
        self.title = title
        self.text = text
        self.creation = datetime.now()
        self.update = datetime.now()

    def __eq__(self, other):
        return (self.code == other.code)
        
    def __repr__(self) -> str:
        return f"Post(Code: {self.code}, Title: {self.title}, Text: {self.text}, Created At: {self.creation}, Last Updated: {self.update})"

    def __str__(self) -> str:
        return f"Title: {self.title}, \nText: {self.text} \nCreated At: {self.creation} \nLast Updated: {self.update}"