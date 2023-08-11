from django.test import TestCase
from store.models import Book
from store.serializers import BooksSerializer

class BooksSerializerTestCase(TestCase):
    def setUp(self):
        self.book_1 = Book.objects.create(name='Test book 1', price=25.00, author_name='Author 1')
        self.book_2 = Book.objects.create(name='Test book 2', price=50.00, author_name='Author 2')

    def test_serialization(self):
        serializer_data = BooksSerializer([self.book_1, self.book_2], many=True).data
        expected_data = [
            {
                'id': self.book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Author 1',
            },
            {
                'id': self.book_2.id,
                'name': 'Test book 2',
                'price': '50.00',
                'author_name': 'Author 2',
            },
        ]

        self.assertEqual(expected_data, serializer_data)
