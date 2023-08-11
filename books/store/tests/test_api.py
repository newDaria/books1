import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Book
from store.serializers import BooksSerializer
from django.contrib.auth.models import User
from decimal import Decimal


class BookApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username', password='testpassword')
        self.book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Author 1')
        self.book_2 = Book.objects.create(name='Test book 2', price=50, author_name='Author 2')
        self.book_3 = Book.objects.create(name='Test book 3', price=75, author_name='Author 3')

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_filter_price(self):
        url = reverse('book-list')
        response = self.client.get(url, {'price': 25})
        serializer_data = BooksSerializer([self.book_1], many=True).data

        # Compare data elements regardless of their order
        for book_data in serializer_data:
            self.assertIn(book_data, response.data)

    def test_ordering_price(self):
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'price'})
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        sorted_data = sorted(serializer_data, key=lambda x: x['price'])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(sorted_data, response.data)

    def test_ordering_author_name(self):
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'author_name'})
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        sorted_data = sorted(serializer_data, key=lambda x: x['author_name'])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(sorted_data, response.data)

    def test_search_name(self):
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Test book 1'})
        serializer_data = BooksSerializer([self.book_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_search_author_name(self):
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Author 2'})
        serializer_data = BooksSerializer([self.book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):

        url = reverse('book-list')
        data = {
            'name': 'New Book',
            'price': '29.99',
            'author_name': 'Author Name',
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4,Book.objects.all().count())
        print(Book.objects.last().owner)
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            'name': self.book_1.name,
            'price': '575.99',
            'author_name': self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(Decimal('575.99'), self.book_1.price)

    def test_delete_book(self):
        url = reverse('book-detail', args=[self.book_1.id])
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Verify the book is deleted
        self.assertFalse(Book.objects.filter(id=self.book_1.id).exists())




