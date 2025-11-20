from blogging.dao.post_dao import PostDAOPickle
from blogging.post import Post
from datetime import datetime
from blogging.__init__ import binary_search


class Blog:
    def __init__(self, id: int, name: str, url: str, email: str) -> None:
        # the unique ID of the blog
        self.id: int = id

        self.postPickle = PostDAOPickle()

        # blog data
        self.name: str = name
        self.url: str = url
        self.email: str = email

        # list of posts in the blog
        self.posts: list[Post] = []

    def set_values(self, id: int, name: str, url: str, email: str) -> None:
        """
        Sets the values of the blog.
        Args: id (int): the unique ID of the blog
                name (str): the name of the blog
                url (str): the URL of the blog
                email (str): the contact email of the blog
        Returns: None
        """

        # Only Update data if it is different
        if self.id != id:
            self.id = id
        if self.name != name:
            self.name = name
        if self.url != url:
            self.url = url
        if self.email != email:
            self.email = email

    def create_post(self, title: str, text: str) -> Post:
        """
        Creates a new post in the blog.
        Args: titie (str): the title of the post
                text (str): the text of the post
        Returns the newly created post
        """

        new_post: Post = Post(0, title, text)
        return self.postPickle.create_post(new_post)

    def search_post(self, code: int):
        """
        Searches for a post given its unique code.
        Args: code (int): the unique code of the post to search for
        Returns the post if found, or None if no post with given code exists
        """
        return self.postPickle.search_post(code)

    def retrieve_posts(self, text: str) -> list[Post]:
        """
        Retrieves all posts given a search text.
        Args: text (str): the text to find in posts

        Returns a list of all posts that contain the search query in the title or text
        """
        return self.postPickle.retrieve_posts(search_string=text)

    def update_post(self, code: int, title: str, text: str) -> Post:
        """
        Updates the a post given the unique code

        Args: code (int): the unique code of the post to update
                title (str): the new title of the post
                text (str): the new text of the post
        Returns the updated post if successful, or None if no post was found
        """
        return self.postPickle.update_post(code, title, text)

    def delete_post(self, code: int) -> bool:
        """
        Deletes a post from the blog given its unique code.

        Args: code (int): the unique code of the post to delete

        Return True if the post was successfully deleted,
        or False if no post with given code exists
        """
        return self.postPickle.delete_post(code)

    def list_posts(self) -> list[Post]:
        """
        Lists the full set of posts from a blog,
        from the last created
        post to the first created post.

        Returns a list of all posts in the blog
        ordered from most recently created to oldest.
        """
        return self.postPickle.list_posts()

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.name == other.name
            and self.url == other.url
            and self.email == other.email
        )

    def __repr__(self) -> str:
        return f"Blog({self.id}, {self.name}, {self.url}, {self.email})"

    def __str__(self) -> str:
        return f"Blog ID: {self.id}. Name: {self.name}. Website: {self.url}. Email: {self.email}"
