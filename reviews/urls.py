from django.contrib import admin
from django.urls import path, include
from . import views, api_views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'books', api_views.BookViewSet)
router.register(r'reviews', api_views.ReviewViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:id>/', views.book_detail, name='book_detail'),
    path("publishers/<int:pk>/", views.publisher_edit, name="publisher_edit"),
    path("publishers/new/", views.publisher_edit, name="publisher_create"),
    path("books/<book_pk>/reviews/new/", views.review_edit, name='review_create'),
    path("books/<book_pk>/reviews/<review_pk>/", views.review_edit, name='review_edit'),
    path("books/<book_pk>/media/", views.book_media, name='book_media'),
#     Đường dẫn cho API
    path('api/first_api_view/', api_views.first_api_view),
    path('api/all_books/', api_views.AllBooks.as_view(), name='all_books'), #as_view() được dùng khi gọi tới lớp của view
    path('api/', include((router.urls, 'api'))),
    path('api/login', api_views.Login.as_view(), name='login')
]