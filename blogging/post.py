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

        self.creation_time: tuple = current_date

        self.update_time: tuple = current_date

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
        self.update_time = updated_date

    def __eq__(self, other):
        return (
            self.code == other.code
            and self.title == other.title
            and self.text == other.text
            and self.creation_time == other.creation_time
            and self.update_time == other.update_time
        )

    def __repr__(self) -> str:
        return f"Post(Code: {self.code}, Title: {self.title}, Text: {self.text}, Created At: {self.creation_time}, Last Updated: {self.update_time})"

    def __str__(self) -> str:
        return f"Title: {self.title}, \nText: {self.text} \nCreated At: {self.creation_time} \nLast Updated: {self.update_time}"
