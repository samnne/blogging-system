from blogging.post import Post
# from post import Post
class Blog:
    def __init__(self, id: int, name:str, url:str, email:str):
        self.id = id
        self.name = name
        self.url = url
        self.email = email
        self.posts: list[Post] = []
    
    
    def set_values(self, id:int, name:str, url:str, email:str):
        if self.id != id:
            self.id = id
        
        if self.name != name:
            self.name = name
        
        if self.url != url:
            self.url = url
        
        if self.email != email:
            self.email = email
        
      
    def create_post(self, title:str, text:str):
        new_code = len(self.posts) + 1
        new_post = Post(new_code, title, text)
        self.posts.append(new_post)
        return new_post
        
    
    def search_post(self, code:int) -> Post | None:
        
        left, right = 0, len(self.posts) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if self.posts[mid].code == code:
                return self.posts[mid]
            elif self.posts[mid].code < code:
                left = mid + 1
            else:
                right = mid - 1
        return None
    
    def retrieve_posts(self, text: str) -> list[Post] | None:
        filtered_list = [post for post in self.posts if text in post.text]
        return filtered_list
        
    
    def __eq__(self, other):
        
        return (self.id == other.id and
                self.name == other.name and
                self.url == other.url and
                self.email == other.email)
    
    def __repr__(self) -> str:
        return f"Blog({self.id}, {self.name}, {self.url}, {self.email})"
    
    
    def __str__(self)->str:
        return f"Blog ID: {self.id}. Name: {self.name}. Website: {self.url}. Email: {self.email}"
    
    
if __name__ == "__main__":
    blog = Blog(1, "2", "3", "5")
    blog.create_post("teteet", "hegrgwgw")
    blog.create_post("teteet", "hegrgwgw")
    blog.create_post("teteet", "hegrgwgw")
    blog.create_post("teteet", "hegrgwgw")
    blog.retrieve_posts("gr11")