from blogging.post import Post

# from post import Post
from datetime import datetime
from blogging.__init__ import binary_search


class Blog:
    def __init__(self, id: int, name: str, url: str, email: str) -> None:
        # the unique ID of the blog
        self.id = id

        # blog data
        self.name = name
        self.url = url
        self.email = email

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

        new_code = len(self.posts) + 1
        new_post = Post(new_code, title, text)
        self.posts.append(new_post)
        return new_post

    def search_post(self, code: int) -> Post | None:
        """
        Searches for a post given its unique code.
        Args: code (int): the unique code of the post to search for
        Returns the post if found, or None if no post with given code exists
        """
        return binary_search(self.posts, code)

    def retrieve_posts(self, text: str) -> list[Post]:
        """
        Retrieves all posts given a search text.
        Args: text (str): the text to find in posts

        Returns a list of all posts that contain the search query in the title or text
        """
        filtered_list = [
            post for post in self.posts if text in post.title or text in post.text
        ]
        return filtered_list

    def update_post(self, code: int, title: str, text: str) -> Post | None:
        """
        Updates the a post given the unique code

        Args: code (int): the unique code of the post to update
                title (str): the new title of the post
                text (str): the new text of the post
        Returns the updated post if successful, or None if no post was found
        """
        post = self.search_post(code)
        if post:
            post.set_values(title, text)
            return post
        return None

    def delete_post(self, code: int) -> bool:
        """
        Deletes a post from the blog given its unique code.

        Args: code (int): the unique code of the post to delete

        Return True if the post was successfully deleted,
        or False if no post with given code exists
        """
        post_to_delete = self.search_post(code)

        if not post_to_delete:
            print("post with given code does not exist")
            return False

        self.posts = [post for post in self.posts if post.code != code]
        return True

    def list_posts(self) -> list[Post]:
        """
        Lists the full set of posts from a blog,
        from the last created
        post to the first created post.

        Returns a list of all posts in the blog
        ordered from most recently created to oldest.
        """
        # Return posts in reverse order from given creation date
        post_in_reverse = self.posts[::-1]
        return post_in_reverse

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


if __name__ == "__main__":
    blog = Blog(1, "2", "3", "5")
    blog.create_post("teteet", "hegrgwgw")
    blog.create_post("teteet", "hegrgwgw")
    blog.create_post("teteet", "hegrgwgw")
    blog.create_post("teteet", "hegrgwgw")
    blog.retrieve_posts("gr11")
