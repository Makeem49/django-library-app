import datetime


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from catalog.forms import RenewBookForm
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
    contain_genre = Book.objects.filter(
        summary__icontains='genre ').all().count()

    num_of_visit = request.session.get('num_of_visit', 0)
    request.session['num_of_visit'] = num_of_visit + 1

    context = {
        'number_of_author': number_of_author,
        'num_of_books': num_of_books,
        'num_of_bookInstance_available': num_of_bookInstance_available,
        'number_of_bookInstance': number_of_bookInstance,
        'num_of_genre': num_of_genre,
        'contain_genre': contain_genre,
        'num_of_visit': num_of_visit
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
class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = 'my_book_list'
    queryset = Book.objects.all()
    paginate_by = 10
    template_name = 'catalog/books.html'


# The below func implement the class view for details of a book
class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    # customizing the context
    context_object_name = 'my_book_details'
    template_name = 'catalog/book_detail.html'


class AuthorDetail(LoginRequiredMixin, generic.DetailView):
    model = Author
    context_object_name = 'author_details'
    template_name = 'catalog/author_details.html'


class AuthorList(LoginRequiredMixin, generic.ListView):
    model = Author
    context_object_name = 'author_list'
    paginate_by = 2
    template_name = 'catalog/author_list.html'


def get_book_detail(request, pk):
    try:
        detail = Book.objects.get(id=pk)
        context = {
            'detail': detail
        }
    except Book.DoesNotExist:
        raise Http404('Book does not exit')

    return render(request, 'catalog/book_detail.html', context=context)


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 1

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_date')


class ShowBorrowedBooks(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required: str = 'catalog.can_mark_returned'
    model = BookInstance
    paginate_by: int = 2
    template_name: str = 'catalog/bookinstance_list_borrowed_book.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_date')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_date = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('catalog-loan-books'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required: str = 'catalog.can_mark_returned'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

    success_url = reverse_lazy('catalog-authors')


class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required: str = 'catalog.can_mark_returned'
    model = Author
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'


class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required: str = 'catalog.can_mark_returned'
    model = Author
    success_url = reverse_lazy('catalog-authors')


class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required: str = 'catalog.can_mark_returned'
    model = Book
    fields = ['title', 'summary', 'isbn', 'author', 'genre', 'language']

    success_url = reverse_lazy('catalog-books')


class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required: str = 'catalog.can_mark_returned'
    model = Book
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'


class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('catalog-authors')
