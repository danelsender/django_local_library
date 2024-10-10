from django.contrib import admin

# Register your models here.

from .models import Author, Genre, Book, BookInstance, Language

class BooksInline(admin.TabularInline):
   model = Book

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
   list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
   fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
   inlines = [BooksInline]
# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

admin.site.register(Genre)
# admin.site.register(BookInstance)
# Define the admin class
class BookInstanceAdmin(admin.ModelAdmin):
   list_display = ('book', 'status', 'due_back', 'id')
   list_filter = ('status', 'due_back')
   fieldsets = (
      (None, {
         'fields': ('book', 'imprint', 'id')
      }),
      ('Availability', {
         'fields': ('status', 'due_back')
      })
   )
# Register the admin class with the associated model
admin.site.register(BookInstance, BookInstanceAdmin)

class BookInstanceInline(admin.TabularInline):
   model = BookInstance

#Define the admin class
class BookAdmin(admin.ModelAdmin):
   # pass
   list_display = ('title', 'author', 'display_genre')
   
   inlines = [BookInstanceInline]
# Register the admin class with the associated model
admin.site.register(Book, BookAdmin)

admin.site.register(Language)