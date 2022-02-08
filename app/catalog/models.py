from datetime import date
from django.db import models
import uuid
from django.urls import reverse

# Create your models here.


class Book(models.Model):
    # Model representation for Book
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField('Title', max_length=100)
    summary = models.TextField(
        "Summary", max_length=2000, help_text="Enter a brief description of the book.")
    # using UUID field for globally unique ID
    isbn = models.CharField('ISBN', max_length=100, unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # relationsship
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(
        'Genre', help_text='Enter a genre for the book.')
    language = models.ForeignKey(
        "Language", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"Book {self.title} is created"

    def get_absolute_url(self):
        return reverse('catalog-book-detail', args=[str(self.id)])

    def display_genre(self):
        for genre in self.genre.all():
            print(f"{genre} ------> genre")
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    def display_author_name(self):
        return f"{self.author.first_name} {self.author.last_name}"

    display_genre.short_description = 'Genre'
    display_author_name.short_description = 'Author name'

class BookInstance(models.Model):
    # Model representation for book instance
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library.')

    # relationship
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    due_date = models.DateField('Due date', null=True, blank=True)
    imprint = models.CharField('Imprint', max_length=200)

    LOAN_STATUS = (
        ('a', 'Available'),
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('r', 'Reserved'),
    )

    status = models.CharField('Status', choices=LOAN_STATUS, max_length=1,
                              default='m', blank=True, help_text='Book availability')

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"Book Instance {self.book.title} created"


class Language(models.Model):
    # Model representation for language
    name = models.CharField("Name", max_length=100,
                            help_text="Enter book language")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} created"


class Genre(models.Model):
    # Model representation for genre
    name = models.CharField(
        'Name', max_length=500, help_text='Enter genre for book e.g (Fiction, Science)')

    def __str__(self):
        return f"{self.name} is created"


class Author(models.Model):
    # Model represntation for Author
    id = models.IntegerField(primary_key=True, unique=True)
    first_name = models.CharField("First name", max_length=100)
    last_name = models.CharField("Last name", max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        return reverse('catalog-author-detail', args=[str(self.id)])

    def __str__(self):
        return f"Author {self.first_name} created."
