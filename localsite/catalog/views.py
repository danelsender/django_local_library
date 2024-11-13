from django.shortcuts import render
from django.views import generic

# Create your views here.
from .models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    
    num_genres = Genre.objects.count()
    
    num_books_with_word = Book.objects.filter(title__icontains='the').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_with_word': num_books_with_word,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
 
class BookListView(generic.ListView):
   model = Book
   context_object_name = 'book_list'
   
   # queryset = Book.objects.filter(title__icontains='the')[:2] # Get 2 books containing the title 'the'
   
   template_name = 'books/book_list.html'
   

class BookDetailView(generic.DetailView):
   model = Book

   def book_detail_view(request, primary_key):
    try:
        book = Book.objects.get(pk=primary_key)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')

    return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):
   
   model = Author
   
   context_object_name = 'author_list'
   
   template_name = 'authors/author_list.html'
   
class AuthorDetailView(generic.DetailView):
   model = Author

   def author_detail_view(request, primary_key):
    try:
        author = Author.objects.get(pk=primary_key)
    except Author.DoesNotExist:
        raise Http404('Author does not exist')

    return render(request, 'catalog/author_detail.html', context={'author': author})
