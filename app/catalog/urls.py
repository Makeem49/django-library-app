from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='catalog-home'),
    path('authors/', views.AuthorList.as_view(), name='catalog-authors'),
    # path('books/', views.books, name='catalog-books'),
    path('books/', views.BookListView.as_view(), name='catalog-books'),
    path('book-detail/<int:pk>', views.BookDetailView.as_view(),
         name='catalog-book-detail'),
    path('author-detail/<int:pk>', views.AuthorDetail.as_view(),
         name='catalog-author-detail'),
    path('librarian/borrowed_books/',
         views.ShowBorrowedBooks.as_view(), name='catalog-loan-books'),
     path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]
