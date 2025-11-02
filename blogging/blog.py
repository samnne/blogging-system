
class Blog:
    def __init__(self, id: int, name:str, url:str, email:str):
        self.id = id
        self.name = name
        self.url = url
        self.email = email
    
    
    def set_values(self, id:int = 0, name:str = "", url:str = "", email:str = ""):
        
        if id:
            self.id = id
        if name:
            self.name = name
        if url: 
            self.url = url
        if email:
            self.email = email
        if not (name or url or email or id):
            print("no values provided to update")
    
    def __eq__(self, other):
        return self.id == other.id
    