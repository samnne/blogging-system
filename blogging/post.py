from datetime import datetime


class Post:
    def __init__(self, code: int, title: str, text: str):
        # auto incremented key / unique ID
        self.code: int = code

        # Post data
        self.title: str = title
        self.text: str = text

        # Timestamps for creation and last update, stored as tuples (year, month, day, hour, minute)
        now = datetime.now()
        current_date = (
            now.year,
            now.month,
            now.day,
            now.hour,
            now.minute,
        )

        self.creation: tuple = current_date

        self.update: tuple = current_date

    def set_values(self, title, text):
        """
        Updates Values of the post given a title and a text
        Args: title (str): the new title
                text (str): the new text for the post
        Returns None
        """
        now = datetime.now()
        updated_date = (
            now.year,
            now.month,
            now.day,
            now.hour,
            now.minute,
        )

        self.title = title
        self.text = text
        self.update = updated_date

    def __eq__(self, other):
        return (
            self.code == other.code
            and self.title == other.title
            and self.text == other.text
            and self.creation == other.creation
            and self.update == other.update
        )

    def __repr__(self) -> str:
        return f"Post(Code: {self.code}, Title: {self.title}, Text: {self.text}, Created At: {self.creation}, Last Updated: {self.update})"

    def __str__(self) -> str:
        return f"Title: {self.title}, \nText: {self.text} \nCreated At: {self.creation} \nLast Updated: {self.update}"
