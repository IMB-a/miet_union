from django.test import TestCase


class TestClass(TestCase):
    def test_simple(self):
        print("Method: test_simple.")
        self.assertEqual(1 + 1, 2)
