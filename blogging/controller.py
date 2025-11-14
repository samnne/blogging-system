from typing import Union
from blogging.blog import Blog
from blogging.post import Post
from blogging.dao.blog_dao import BlogDAOJSON
from blogging.__init__ import get_password_hash, raise_exception
from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException


class Controller:

    def __init__(self) -> None:
        self.user: dict[str, str] = {
            "user": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
            "ali": "6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810",
            "kala": "e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e",
        }

        self.is_logged_in: bool = False
        self.blogs: list[Blog] = []
        self.blogJSON = BlogDAOJSON()
        self.current_blog: Blog = None  # type:ignore

    # LOG IN/OUT METHODS
    def login(self, username: str, password: str) -> bool:
        if self.is_logged_in:
            raise_exception(exception=DuplicateLoginException)

        for key, value in self.user.items():
            if key == username and value == get_password_hash(password=password):
                self.is_logged_in = True
                return True

        raise InvalidLoginException

    def logout(self):
        if not self.is_logged_in:
            raise_exception(InvalidLogoutException, "Can't log out if not logged in")

        self.is_logged_in = False
        return True

    # CRUD FOR BLOG'S GIVEN A CURRENT USER
    def search_blog(self, id: int) -> Union[Blog, None]:
        """
        Search for a blog by its unique ID.
        Args: id (int): Unique ID of the blog to search for
        Returns: the Blog if found, or None if not found
        """
        if not self.is_logged_in:
            raise_exception(IllegalAccessException, "must be logged in to search blogs")

        return self.blogJSON.search_blog(id)

    def create_blog(self, id: int, name: str, url: str, email: str) -> Blog:
        """
        Create a New Blog with the given parameters.
        Returns None if there already exists a blog with the attempted ID.

        Args: id (int): Unique ID for the blog
                name (str): Name of the blog
                url (str): URL of the blog
                email (str): Contact email for the blog
        Returns: The created Blog or None if creation failed
        """
        if not self.is_logged_in:
            raise_exception(
                IllegalAccessException, "must be logged in to create a blog"
            )

        if self.search_blog(id):
            raise_exception(
                IllegalOperationException, "blog with given id already exists"
            )
        new_blog: Blog = Blog(id, name, url, email)
        return self.blogJSON.create_blog(new_blog)

    def retrieve_blogs(self, search_string: str) -> list[Blog]:
        """
        Retrieve blogs whose name contains the given filter string.

        Args: name (str): The fuzzy find filter string
        Returns list of blogs or raises an error
        """
        if not self.is_logged_in:
            raise_exception(IllegalAccessException, "must be logged in to search blogs")

        return self.blogJSON.retrieve_blogs(search_string)

    def update_blog(
        self, search_id, new_id: int, name: str, url: str, email: str
    ) -> bool:
        """
        Update the blog with the given ID using the provided parameters.
        Only non-empty parameters will be used to update the blog.

        Args: id (int): Unique ID for the blog to be updated
                name (str): New name of the blog
                url (str): New URL of the blog
                email (str): New contact email for the blog
        Returns: True if update was successful, False if blog not found,
        throws an error if not logged in
        """
        if not self.is_logged_in:

            raise_exception(
                IllegalAccessException, "must be logged in to update a blog"
            )

        if self.current_blog and self.current_blog.id == search_id:
            raise_exception(IllegalOperationException, "cannot update current blog")

        return self.blogJSON.update_blog(
            key=search_id, blog=Blog(new_id, name, url, email)
        )

    def delete_blog(self, id: int) -> bool:
        """
        Delete the blog by ID

        Args: id (int): Unique ID for the blog to be deleted
        Returns: True if deletion was successful, False if blog not found,
        None if not logged in
        """

        if not self.is_logged_in:
            raise_exception(
                IllegalAccessException, "must be logged in to delete a blog"
            )

        if self.current_blog and self.current_blog.id == id:
            raise_exception(IllegalOperationException, "Cannot delete current Blog")
        return self.blogJSON.delete_blog(id)

    def list_blogs(self) -> list[Blog]:
        """
        List all blogs in the system.
        Args: None
        Returns: a list of all the blogs in the system.
        """
        if not self.is_logged_in:
            raise_exception(
                IllegalAccessException, "can't list blogs when not logged in"
            )
        return self.blogJSON.list_blogs()

    def set_current_blog(self, id: int) -> None:
        """
        Sets the current blog
        Args: id (int), the unique ID of the blog to set as current
        Returns: None
        """
        if not self.is_logged_in:
            raise_exception(
                IllegalAccessException, "must be logged in to set current blog"
            )

        search_blog: Blog | None = self.search_blog(id)
        if not search_blog:
            raise_exception(
                IllegalOperationException, "cannot set a blog that doesnt exist"
            )

        self.current_blog = search_blog  # type: ignore

    def get_current_blog(self) -> Union[Blog, None]:
        """
        Gets the current blog
        Args: None
        Returns the current Blog or nothing
        """
        if not self.is_logged_in:
            raise_exception(
                IllegalAccessException, "must be logged in to get current blog"
            )

        if not self.current_blog:
            return None

        return self.current_blog

    def unset_current_blog(self) -> None:
        """
        Unsets the current blog
        Args: None
        Returns: None
        """
        if not self.is_logged_in:
            raise_exception(IllegalAccessException, "must be logged in to unset blog")

        self.current_blog = None  # type: ignore

    # CRUD FOR POST'S GIVEN A CURRENT BLOG

    def create_post(self, title: str, text: str) -> Post:
        """
        Creates a new post given a current blog
        Args: title (str), the title of the post
                text (str), the text of the post
        Returns the newly created post
        """

        if not self.is_logged_in:
            raise_exception(
                IllegalAccessException, "can't create a post without being logged in"
            )

        if not self.current_blog:
            raise_exception(NoCurrentBlogException, "No current blog set")

        return self.current_blog.create_post(title=title, text=text)

    def search_post(self, code: int):
        """
        Searches for the post given the current code
        """

        if not self.is_logged_in:
            raise_exception(
                IllegalAccessException, "can't search a post without being logged in"
            )

        if not self.current_blog:
            raise_exception(NoCurrentBlogException, "No current blog set")

        return self.current_blog.search_post(code)

    def retrieve_posts(self, text: str) -> Union[list[Post], None]:
        """
        Retrieves all the post given a text search string

        Args: text (str), the text to find
        Returns a list of all posts that contain that text in the post
        """
        if not self.is_logged_in:
            raise_exception(
                IllegalAccessException, "can't retrieve posts without being logged in"
            )

        if not self.current_blog:
            raise_exception(NoCurrentBlogException, "No current blog set")

        return self.current_blog.retrieve_posts(text)

    def update_post(self, code: int, title: str, text: str) -> Post:
        """
        Updates a post given the code, title and text

        Args: code (int), the unique code of the post
              title (str), the new title of the post
              text (str), the new text of the post
        Returns the updated post or None if not found
        """
        if not self.is_logged_in:
            raise_exception(
                IllegalAccessException, "can't update a post without being logged in"
            )

        if not self.current_blog:
            raise_exception(NoCurrentBlogException, "No current blog set")

        return self.current_blog.update_post(code, title, text)

    def delete_post(self, code: int) -> bool:
        """
        Deletes a post given the code

        Args: code (int), the unique code of the post
        Returns True if deleted, False if not found, None if not logged in or no current blog
        """
        if not self.is_logged_in:
            raise_exception(
                IllegalAccessException, "can't delete a post without being logged in"
            )

        if not self.current_blog:
            raise_exception(NoCurrentBlogException, "No current blog set")

        return self.current_blog.delete_post(code)

    def list_posts(self) -> list[Post]:
        """
        Lists all posts in the current blog
        Args: None
        Returns a list of all posts in the current blog

        """
        if not self.is_logged_in:
            raise_exception(
                IllegalAccessException, "can't list posts without being logged in"
            )

        if not self.current_blog:
            raise_exception(NoCurrentBlogException, "No current blog set")

        return self.current_blog.list_posts()


if __name__ == "__main__":
    controller = Controller()
    controller.login("user", "123456")
    controller.create_blog(1, "sam", "new_sam", "fwf")

    controller.delete_blog(1)
