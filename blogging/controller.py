from blogging.blog import Blog


class Controller:

    def __init__(self) -> None:
        self.user: dict[str, str] = {
            "username": "user", "password": "blogging2025"}
        self.is_logged_in: bool = False
        self.blogs: list[Blog] = []

    def login(self, username: str, password: str) -> bool | None:
        if self.is_logged_in:
            print("cannot login again while still logged in")
            return None

        if self.user["username"] != username:
            return False

        if self.user["password"] != password:
            return False

        self.is_logged_in = True
        return True

    def logout(self):
        if self.is_logged_in == False:
            print("log out only after being logged in")
            return

        self.is_logged_in = False
        return True

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
        new_blog = Blog(id, name, url, email)
        self.blogs.append(new_blog)
        self.blogs.sort(key=lambda blog: blog.id)
        return new_blog

    def search_blog(self, id: int) -> Blog | None:
        """
        Search for a blog by its unique ID.
        """

        if not self.is_logged_in:
            print("must be logged in to search blogs")
            return None

        left, right = 0, len(self.blogs) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.blogs[mid].id == id:
                return self.blogs[mid]
            elif self.blogs[mid].id < id:
                left = mid+1
            else:
                right = mid - 1
        return None

    def retrieve_blogs(self, ff_name: str) -> list[Blog] | None:
        """
        Retrieve blogs whose name contains the given filter string.

        Args: ff_name (str): The fizzy find filter string
        """
        if not self.is_logged_in:
            print("must be logged in to search blogs")
            return None

        filtered_blogs: list[Blog] = [
            blog for blog in self.blogs if ff_name in blog.name]
        return filtered_blogs


    def update_blog(self,search_id,  new_id: int, name: str = "", url: str = "", email: str = "") -> bool | None:
        """
        Update the blog with the given ID using the provided parameters.
        Only non-empty parameters will be used to update the blog.

        Args: id (int): Unique ID for the blog to be updated
                name (str): New name of the blog
                url (str): New URL of the blog
                email (str): New contact email for the blog
        Returns: True if update was successful, False if blog not found, None if not logged in
        """
        if not self.is_logged_in:
            print("must be logged in to update a blog")
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


if __name__ == "__main__":
    controller = Controller()
    controller.login("user", "blogging2025")
