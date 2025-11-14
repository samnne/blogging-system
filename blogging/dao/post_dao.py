from abc import ABC, abstractmethod
from blogging.post import Post

from blogging import binary_search


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

    def __init__(self):
        self.posts = []

    def search_post(self, key):

        return binary_search(self.posts, key)

    def create_post(self, post):
        post.code = len(self.posts) + 1
        self.posts.append(post)
        return post

    def retrieve_posts(self, search_string):
        filtered_list: list[Post] = [
            post
            for post in self.posts
            if search_string in post.title or search_string in post.text
        ]

        return filtered_list

    def update_post(self, key, new_title, new_text):
        post: Post | None = self.search_post(key)
        if post:
            post.set_values(new_title, new_text)
            return post
        return None

    def delete_post(self, key):
        post_to_delete = self.search_post(key)

        if not post_to_delete:
            print("post with given code does not exist")
            return False

        self.posts = [post for post in self.posts if post.code != key]

        return True

    def list_posts(self):
        post_in_reverse: list[Post] = self.posts[::-1]
        return post_in_reverse
