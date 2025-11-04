from unittest import TestCase
import unittest
from blogging.post import Post
from blogging.blog import Blog


class PostTest(TestCase):

    def setUp(self):
        self.blog = Blog(1, "Name", "URL", "email")

    def test_list_posts(self):

        expected_post = Post(1, "WSG", "Updated")
        expected_post2 = Post(2, "Next Title", "Text 2")
        expected_post3 = Post(3, "Super Next Title", "Text 3")

        self.blog.create_post("New Title", "Text")
        self.blog.create_post("Next Title", "Text 2")
        self.blog.create_post("Super Next Title", "Text 3")

        # Test that posts is ordered by creation date and handles mutation
        self.blog.update_post(1, "WSG", text="Updated")
        actual_list = self.blog.list_posts()

        self.assertEqual(3, len(actual_list))
        self.assertEqual(expected_post, actual_list[2])
        self.assertEqual(expected_post2, actual_list[1])
        self.assertEqual(expected_post3, actual_list[0])


if __name__ == "__main__":
    unittest.main()
