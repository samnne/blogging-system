from json import JSONDecoder, JSONEncoder

from blogging.blog import Blog


class BlogEncoder(JSONEncoder):
    """
    The encoder to format it into the file
    """

    def default(self, obj):
        if isinstance(obj, Blog):
            return {
                "__type__": "Blog",
                "id": obj.id,
                "name": obj.name,
                "email": obj.email,
                "url": obj.url,
            }
        return super().default(obj)


class BlogDecoder(JSONDecoder):
    """
    The decoder to convert the file data to Blog Objects
    """

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        if "__type__" in dct and dct["__type__"] == "Blog":
            return Blog(
                id=dct["id"], name=dct["name"], email=dct["email"], url=dct["url"]
            )
