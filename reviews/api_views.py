from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Review
from .serializers import (BookSerializer, ReviewSerializer)
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView

@api_view()
def first_api_view(request):
    num_books = Book.objects.count()
    return Response({'num_books': num_books})


# Đoạn này dùng cho khi trong file api_views mình tạo lại các trường của đối tượng
# @api_view()
# def all_books(request):
#     books = Book.objects.all()
#     book_serializer = BookSerializer(books, many=True)
#     return Response(book_serializer.data)


# Được sử dụng khi các đối tượng trong api_view kế thừa lại model của dối tượng
class AllBooks(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     pagination_class = LimitOffsetPagination
#     authentication_classes = []


class Login(APIView):

    def post(self, request):
        user = authenticate(username=request.data.get("username"),
                            password=request.data.get("password"))
        if not user:
            return Response({'error': "Credentials are incorrect or user is does not exist"},
                            status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=HTTP_200_OK)


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    # authentication_classes = []

