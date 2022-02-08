from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='catalog-home'),
    path('author-details/', views.AuthorList.as_view(), name='catalog-authors'),
    # path('books/', views.books, name='catalog-books'),
    path('books/', views.BookListView.as_view(), name='catalog-books'),
    path('book-detail/<int:pk>', views.get_book_detail, name='catalog-book-detail'),
    path('author-detail/<int:pk>', views.AuthorDetail.as_view(), name='catalog-author-detail')
]

