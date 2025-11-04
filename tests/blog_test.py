from unittest import TestCase
import unittest
from blogging.blog import Blog
from blogging.post import Post


class BlogTest(TestCase):

    def setUp(self):
        self.blog = Blog(1, "Name", "URL", "email")

    def test_new_blog(self):
        expected_blog = Blog(2, "Second Name", "URL2", "email2")
        expected_blog2 = Blog(5, "Second Name", "Url", "email2")

        self.assertNotEqual(expected_blog, self.blog, "Blog's aren't equal to start")
        self.blog.set_values(2, "Second Name", "URL2", "email2")
        self.assertEqual(expected_blog, self.blog, "Blog's are infact equal")

        self.blog.set_values(5, self.blog.name, "Url", self.blog.email)
        self.assertEqual(expected_blog2, self.blog, "Blog's are infact equal")


if __name__ == "__main__":
    unittest.main()

