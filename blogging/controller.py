from blogging.blog import Blog
from blogging.post import Post
from blogging.__init__ import binary_search, get_password_hash
from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.duplicate_login_exception import DuplicateLoginException


class Controller:

    def __init__(self) -> None:
        self.user: dict[str, str] = {
            "user": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
            "ali": "6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810",
            "kala": "e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e"
        }
        self.is_logged_in: bool = False
        self.blogs: list[Blog] = []
        self.current_blog: Blog | None = None

    # LOG IN/OUT METHODS
    def login(self, username: str, password: str) -> bool | None:
        if self.is_logged_in:
            print("cannot login again while still logged in")
            raise DuplicateLoginException

        for key,value in self.user.items():
            if key == username and value == get_password_hash(password=password):
                self.is_logged_in = True
                return True
        
        raise InvalidLoginException
      

    def logout(self):
        if not self.is_logged_in:
            print("log out only after being logged in")
            raise InvalidLogoutException

        self.is_logged_in = False
        return True

    # CRUD FOR BLOG'S GIVEN A CURRENT USER
    def search_blog(self, id: int) -> Blog | None:
        """
        Search for a blog by its unique ID.
        Args: id (int): Unique ID of the blog to search for
        Returns: the Blog if found, or None if not found
        """

        if not self.is_logged_in:
            print("must be logged in to search blogs")
            return None

        sorted_blogs: list[Blog] = sorted(self.blogs, key=lambda blog: blog.id)
        return binary_search(sorted_blogs, id)

    def create_blog(self, id: int, name: str, url: str, email: str) -> Blog | None:
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
            print("must be logged in to create a blog")
            return None

        if self.search_blog(id):
            print("blog with given id already exists")
            return None
        new_blog: Blog = Blog(id, name, url, email)
        self.blogs.append(new_blog)

        return new_blog

    def retrieve_blogs(self, name: str) -> list[Blog] | None:
        """
        Retrieve blogs whose name contains the given filter string.

        Args: name (str): The fuzzy find filter string
        """
        if not self.is_logged_in:
            print("must be logged in to search blogs")
            return None

        filtered_blogs: list[Blog] = [blog for blog in self.blogs if name in blog.name]
        return filtered_blogs

    def update_blog(
        self, search_id, new_id: int, name: str, url: str, email: str
    ) -> bool | None:
        """
        Update the blog with the given ID using the provided parameters.
        Only non-empty parameters will be used to update the blog.

        Args: id (int): Unique ID for the blog to be updated
                name (str): New name of the blog
                url (str): New URL of the blog
                email (str): New contact email for the blog
        Returns: True if update was successful, False if blog not found,
        None if not logged in
        """
        if not self.is_logged_in:
            print("must be logged in to update a blog")
            return None

        if self.current_blog and self.current_blog.id == search_id:
            return None

        blog_to_update = self.search_blog(search_id)
        if not blog_to_update:
            print("blog with given id does not exist")
            return False

        if new_id != search_id and self.search_blog(new_id):
            print("blog with new id already exists")
            return False
        blog_to_update.set_values(id=new_id, name=name, url=url, email=email)
        return True

    def delete_blog(self, id: int) -> bool | None:
        """
        Delete the blog by ID

        Args: id (int): Unique ID for the blog to be deleted
        Returns: True if deletion was successful, False if blog not found,
        None if not logged in
        """

        if not self.is_logged_in:
            print("must be logged in to delete a blog")
            return None

        if self.current_blog and self.current_blog.id == id:
            return None

        blog_to_delete = self.search_blog(id)
        if not blog_to_delete:
            print("blog with given id does not exist")
            return False

        self.blogs = [blog for blog in self.blogs if blog.id != id]
        return True

    def list_blogs(self) -> list[Blog] | None:
        """
        List all blogs in the system.
        Args: None
        Returns: a list of all the blogs in the system.
        """
        if not self.is_logged_in:
            print("must be logged in to list blogs")
            return None
        return self.blogs

    def set_current_blog(self, id: int) -> None:
        """
        Sets the current blog
        Args: id (int), the unique ID of the blog to set as current
        Returns: None
        """
        if not self.is_logged_in:
            print("must be logged in to set current blog")
            return None

        search_blog: Blog | None = self.search_blog(id)
        if not search_blog:
            print("cannot set a blog that doesnt exist")
            return None

        self.current_blog = search_blog

    def get_current_blog(self) -> Blog | None:
        """
        Gets the current blog
        Args: None
        Returns the current Blog or nothing
        """
        if not self.is_logged_in:
            print("must be logged in to get current blog")
            return None

        if not self.current_blog:
            print("No current blog set")
            return None

        return self.current_blog

    def unset_current_blog(self) -> None:
        """
        Unsets the current blog
        Args: None
        Returns: None
        """
        if not self.is_logged_in:
            print("must be logged in to unset current blog")
            return None

        self.current_blog = None

    # CRUD FOR POST'S GIVEN A CURRENT BLOG

    def create_post(self, title: str, text: str) -> Post | None:
        """
        Creates a new post given a current blog
        Args: title (str), the title of the post
                text (str), the text of the post
        Returns the newly created post
        """

        if not self.is_logged_in:
            print("must be logged in to get current blog")
            return None

        if not self.current_blog:
            print("No current blog set")
            return None

        return self.current_blog.create_post(title=title, text=text)

    def search_post(self, code: int):
        """
        Searches for the post given the current code
        """

        if not self.is_logged_in:
            print("must be logged in to get current blog")
            return None

        if not self.current_blog:
            print("No current blog set")
            return None

        return self.current_blog.search_post(code)

    def retrieve_posts(self, text: str) -> list[Post] | None:
        """
        Retrieves all the post given a text search string

        Args: text (str), the text to find
        Returns a list of all posts that contain that text in the post
        """
        if not self.is_logged_in:
            print("must be logged in to get current blog")
            return None

        if not self.current_blog:
            print("No current blog set")
            return None

        return self.current_blog.retrieve_posts(text)

    def update_post(self, code: int, title: str, text: str) -> Post | None:
        """
        Updates a post given the code, title and text

        Args: code (int), the unique code of the post
              title (str), the new title of the post
              text (str), the new text of the post
        Returns the updated post or None if not found
        """
        if not self.is_logged_in:
            print("must be logged in to get current blog")
            return None

        if not self.current_blog:
            print("No current blog set")
            return None

        return self.current_blog.update_post(code, title, text)

    def delete_post(self, code: int) -> bool | None:
        """
        Deletes a post given the code

        Args: code (int), the unique code of the post
        Returns True if deleted, False if not found, None if not logged in or no current blog
        """
        if not self.is_logged_in:
            print("must be logged in to get current blog")
            return None

        if not self.current_blog:
            print("No current blog set")
            return None

        return self.current_blog.delete_post(code)

    def list_posts(self) -> list[Post] | None:
        """
        Lists all posts in the current blog
        Args: None
        Returns a list of all posts in the current blog

        """
        if not self.is_logged_in:
            print("must be logged in to get current blog")
            return None

        if not self.current_blog:
            print("No current blog set")
            return None

        return self.current_blog.list_posts()

if __name__ == "__main__":
    controller = Controller()
    controller.login("user", "")