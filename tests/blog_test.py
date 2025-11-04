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

    def test_list_posts(self):

        expected_post = Post(1, "WSG", "Updated")
        expected_post2 = Post(2, "Next Title", "Text 2")
        expected_post3 = Post(3, "Super Next Title", "Text 3")

        self.blog.create_post("New Title", "Text")
        self.blog.create_post("Next Title", "Text 2")
        self.blog.create_post("Super Next Title", "Text 3")
        self.blog.update_post(1, "WSG", text="Updated")

        # Test that posts is ordered by creation date and handles mutation
        actual_list = self.blog.list_posts()

        self.assertEqual(3, len(actual_list))
        self.assertEqual(expected_post, actual_list[2])
        self.assertEqual(expected_post2, actual_list[1])
        self.assertEqual(expected_post3, actual_list[0])


if __name__ == "__main__":
    unittest.main()

