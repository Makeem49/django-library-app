from pydoc import render_doc
from django.shortcuts import render
from django.http import HttpResponse
from .models import Author, Book, BookInstance, Genre

# Create your views here.


def home(request):
    # creating a home view handling incoming http request

    number_of_author = Author.objects.all().count()
    num_of_books = Book.objects.all().count()
    num_of_bookInstance_available = BookInstance.objects.filter(
        status__exact='a').count()
    number_of_bookInstance = BookInstance.objects.all().count()
    num_of_genre = Genre.objects.all().count()
    contain_genre = Book.objects.filter(summary__icontains='genre ').all().count()


    context = {
        'number_of_author': number_of_author,
        'num_of_books': num_of_books,
        'num_of_bookInstance_available': num_of_bookInstance_available,
        'number_of_bookInstance': number_of_bookInstance,
        'num_of_genre' : num_of_genre,
        'contain_genre' : contain_genre
    }

    return render(request, 'home.html', context=context)


def about(request):
    return HttpResponse('About page')


def faq(request):
    return HttpResponse('Frequestly asked question page')
