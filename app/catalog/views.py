from pydoc import render_doc
from pyexpat import model
from re import template
from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Author, Book, BookInstance, Genre
from django.views import generic

# Create your views here.


def home(request):
    # creating a home view handling incoming http request

    number_of_author = Author.objects.all().count()
    num_of_books = Book.objects.all().count()
    num_of_bookInstance_available = BookInstance.objects.filter(
        status__exact='a').count()
    number_of_bookInstance = BookInstance.objects.all().count()
    num_of_genre = Genre.objects.all().count()
    contain_genre = Book.objects.filter(
        summary__icontains='genre ').all().count()

    context = {
        'number_of_author': number_of_author,
        'num_of_books': num_of_books,
        'num_of_bookInstance_available': num_of_bookInstance_available,
        'number_of_bookInstance': number_of_bookInstance,
        'num_of_genre': num_of_genre,
        'contain_genre': contain_genre
    }

    return render(request, 'home.html', context=context)

# the below func implement how to get list of books in function view
def books(request):
    # This view does the same thing the BookListView will do
    available_books = Book.objects.all()

    context = {
        "available_books": available_books
    }
    return render(request, 'catalog/books.html', context=context)


# The below func implement the class view for listing books
class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'
    queryset = Book.objects.all()
    template_name = 'catalog/books.html'


# The below func implement the class view for details of a book
class BookDetailView(generic.DetailView):
    model = Book
    # customizing the context

    context_object_name = 'my_book_details'
    template_name = 'catalog/book_detail.html'


class AuthorDetail(generic.DetailView):
    model = Author
    context_object_name = 'author_details'
    template_name = 'catalog/author_details.html'

class AuthorList(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'catalog/author_list.html'

def get_book_detail(request, pk):
    try:
        detail = Book.objects.get(id=pk)
        context = {
            'detail' : detail
        }
    except Book.DoesNotExist:
        raise Http404('Book does not exit')

    return render(request, 'catalog/book_detail.html', context=context)

