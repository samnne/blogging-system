from abc import ABC, abstractmethod
import pickle
from blogging.configuration import Configuration
from blogging.post import Post

from blogging import binary_search, pickle_update_file


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

        self.posts = []
        self.autosave = Configuration.autosave
        self.blog_records_file = (
            Configuration.records_path + f"/{blog.id}" + Configuration.records_extension
        )
        self.posts: list[Post] = []
        try:
            file = open(self.blog_records_file, "rb")
            self.posts = [] if len(file.readlines()) < 2 else pickle.load(file)
            file.close()
        except Exception:
            print("file error")
            file = open(self.blog_records_file, "wb")
            pickle.dump(self.posts, file)
            file.close()

    def search_post(self, key: int):  # type: ignore
        """
        DAO implementaion of search_post
        """
        return binary_search(self.posts, key)

    def create_post(self, post: Post):  # type: ignore
        """
        DAO implementaion of create_post
        """
        post.code = len(self.posts) + 1
        self.posts.append(post)
        if self.autosave:
            pickle_update_file(self.posts, self.blog_records_file)
        return post

    def retrieve_posts(self, search_string: str):  # type: ignore
        """
        Retrieves all the post given a text search string

        Args: search_string (str), the text to find
        Returns a list of all posts that contain that text in the post
        """
        filtered_list: list[Post] = [
            post
            for post in self.posts
            if search_string in post.title or search_string in post.text
        ]

        return filtered_list

    def update_post(self, key: int, new_title: str, new_text: str):  # type: ignore

        post = self.search_post(key)
        if post:
            post.set_values(new_title, new_text)
            return post
        return None

    def delete_post(self, key: int):  # type: ignore

        post_to_delete: Post = self.search_post(key)  # type: ignore

        if not post_to_delete:
            print("post with given code does not exist")
            return False

        self.posts = [post for post in self.posts if post.code != key]

        return True

    def list_posts(self):  # type: ignore

        post_in_reverse: list[Post] = self.posts[::-1]
        return post_in_reverse
