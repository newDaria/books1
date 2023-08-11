from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from store.models import Book
from store.serializers import BooksSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


# Create your views here.
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]  # You can add other filter backends as needed
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_fields = ['price']  # Define the fields you want to filter on
    ordering_fields = ['price', 'author_name']  # Define the fields you want to allow ordering on
    search_fields = ['name', 'author_name']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

def auth(request):
    return render(request, 'oauth.html')

