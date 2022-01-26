from django.contrib import admin
from .models import Author, Book, BookInstance, Genre, Language

# Register your models here.

# admin.site.register(Author, AuthorAdmin)
# admin.site.register(Book)
# admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)

# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')

# admin.site.register(Author, AuthorAdmin)

# The AuthorAdmin class can also be register with decorator as below

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',
                    'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_author_name', 'display_genre')

    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('status', 'due_date', 'book', 'id')
    list_filter = ('due_date', 'status')

    fieldsets = (
        ("None", {
            "fields":  ('imprint', 'book', 'id')
        }),
        ('Availability', {
            'fields': ('due_date', 'status')
        })
    )
