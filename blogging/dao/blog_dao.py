from abc import ABC, abstractmethod
import json
from blogging.configuration import Configuration
from blogging.__init__ import binary_search, json_update_file, raise_exception
from blogging.blog import Blog
from blogging.dao.blog_encoder_decoder import BlogDecoder, BlogEncoder
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException


class BlogDAO(ABC):

    @abstractmethod
    def search_blog(self, key):
        pass

    @abstractmethod
    def create_blog(self, blog):
        pass

    @abstractmethod
    def retrieve_blogs(self, search_string):
        pass

    @abstractmethod
    def update_blog(self, key, blog):
        pass

    @abstractmethod
    def delete_blog(self, key):
        pass

    @abstractmethod
    def list_blogs(self):
        pass


class BlogDAOJSON(BlogDAO):
    def __init__(self):
        self.autosave = Configuration.autosave
        self.blogs_file = Configuration.blogs_file
        self.blogs = []
        try:
            file = open(self.blogs_file, "r")
            file_data = file.read()
            self.blogs = [] if not file_data else json.loads(file_data, cls=BlogDecoder)
            file.close()
        except FileNotFoundError as FileError:
            print(f"FILE ERROR ###{FileError}###")
            json_update_file(self.blogs, self.blogs_file, Encoder=BlogEncoder)

    def search_blog(self, key: int):
        """
        Search for a blog by its unique ID.
        Args: id (int): Unique ID of the blog to search for
        Returns: the Blog if found, or None if not found
        """

        sorted_blogs: list[Blog] = sorted(self.blogs, key=lambda blog: blog.id)
        return binary_search(sorted_blogs, key)

    def create_blog(self, blog):
        """
        Create a New Blog with the given parameters.
        Returns None if there already exists a blog with the attempted ID.

        Args: id (int): Unique ID for the blog
                name (str): Name of the blog
                url (str): URL of the blog
                email (str): Contact email for the blog
        Returns: The created Blog or None if creation failed
        """
        self.blogs.append(blog)
        if self.autosave:
            json_update_file(
                payload=self.blogs, dest_file=self.blogs_file, Encoder=BlogEncoder
            )

        return blog

    def retrieve_blogs(self, search_string: str) -> list[Blog]:
        """
        Retrieve blogs whose name contains the given filter string.

        Args: name (str): The fuzzy find filter string
        Returns list of blogs or raises an error
        """
        filtered_blogs: list[Blog] = [
            blog for blog in self.blogs if search_string in blog.name
        ]
        return filtered_blogs

    def update_blog(self, key, blog) -> bool:
        """
        Update the blog with the given ID using the provided parameters.
        Only non-empty parameters will be used to update the blog.

        Args: key: unique ID, and blog: new Blog
        Returns: True if update was successful, False if blog not found,
        throws an error if not logged in
        """

        blog_to_update = self.search_blog(key)
        if not blog_to_update:
            raise_exception(
                IllegalOperationException, "cannot update blog that doesnt exist"
            )

        if blog.id != key and self.search_blog(blog.id):
            raise_exception(
                IllegalOperationException, "cannot update one blog with conflicting ID"
            )

        blog_to_update.set_values(id=blog.id, name=blog.name, url=blog.url, email=blog.email)  # type: ignore
        if self.autosave:
            json_update_file(self.blogs, self.blogs_file, Encoder=BlogEncoder)
        return True

    def delete_blog(self, key: int) -> bool:
        """
        Delete the blog by ID

        Args: key (int): Unique ID for the blog to be deleted
        Returns: True if deletion was successful, False if blog not found,
        None if not logged in
        """
        blog_to_delete = self.search_blog(key)
        if not blog_to_delete:
            raise_exception(
                IllegalOperationException, "cannot delete a blog that doesnt exist"
            )

        self.blogs = [blog for blog in self.blogs if blog.id != key]
        if self.autosave:
            json_update_file(self.blogs, self.blogs_file, Encoder=BlogEncoder)
        return True

    def list_blogs(self) -> list[Blog]:
        """
        List all blogs in the system.
        Args: None
        Returns: a list of all the blogs in the system.
        """
        return self.blogs

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


if __name__ == "__main__":
    blogj = BlogDAOJSON()

    blogj.create_blog(Blog(1, "s", "s", "s"))
