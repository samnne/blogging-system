from abc import ABC, abstractmethod
import pickle
from blogging.configuration import Configuration
from blogging.post import Post

from blogging.helper import binary_search, pickle_update_file


class PostDAO(ABC):
    @abstractmethod
    def search_post(self, key):
        pass

    @abstractmethod
    def create_post(self, post):
        pass

    @abstractmethod
    def retrieve_posts(self, search_string):
        pass

    @abstractmethod
    def update_post(self, key, new_title, new_text):
        pass

    @abstractmethod
    def delete_post(self, key):
        pass

    @abstractmethod
    def list_posts(self):
        pass


class PostDAOPickle(PostDAO):

    def __init__(self, blog):

        # Persistence variables and config
        self.autosave = Configuration.autosave
        self.blog = blog
        self.blog_records_file = (
            Configuration.records_path
            + f"/{self.blog.id}"
            + Configuration.records_extension
        )
        # the posts array
        self.posts: list[Post] = []
        if self.autosave:

            try:
                # if there are posts set the counter to the maximum value
                with open(self.blog_records_file, "rb") as file:
                    self.posts = pickle.load(file)
                    if self.posts:
                        self.blog.counter = self.posts[-1].code
            except Exception as e:
            
                # create the new file with an empty array initalized
                pickle_update_file(self.posts, self.blog_records_file)

    def search_post(self, key: int):
        """
        DAO implementaion of search_post
        searches to find the post given current blog
        Args: key (int) -> the unique key to search for
        Return: The post or none if it can't be found
        """
        return binary_search(self.posts, key)

    def create_post(self, post: Post):
        """
        DAO implementaion of create_post
        Args: post (Post) -> the new post to be created
        Returns the created post
        """
        self.blog.counter += 1
        post.code = self.blog.counter
        self.posts.append(post)
        if self.autosave:
            # only save if autosave is true
            pickle_update_file(self.posts, self.blog_records_file)
        return post

    def retrieve_posts(self, search_string: str):
        """
        Retrieves all the post given a text search string

        Args: search_string (str), the text to find
        Returns a list of all posts that contain that text in the post
        """
        filtered_list: list[Post] = [
            post
            for post in self.posts
            # fileter by search_string
            if search_string.lower() in post.title.lower() or search_string.lower() in post.text.lower()
        ]

        return filtered_list

    def update_post(self, key: int, new_title: str, new_text: str):

        post = self.search_post(key)
        if post:
            post.set_values(new_title, new_text)
            if self.autosave:
                # only save if autosave is true
                pickle_update_file(self.posts, self.blog_records_file)
            return post
        return None

    def delete_post(self, key: int):
        post_to_delete = self.search_post(key)

        if not post_to_delete:
            print("post with given code does not exist")
            return False

        self.blog.counter -= 1

        self.posts = [post for post in self.posts if post.code != key]

        if self.autosave:
            # only save if autosave is true
            pickle_update_file(self.posts, self.blog_records_file)
        return True

    def list_posts(self):  # type: ignore

        post_in_reverse: list[Post] = self.posts[::-1]
        return post_in_reverse
