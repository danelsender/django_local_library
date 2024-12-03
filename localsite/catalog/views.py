from catalog.forms import RenewBookForm

import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404

from django.urls import reverse

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
 

@login_required
@permission_required('catalog.can_mark_returned', 
                     raise_exception=True)
def renew_book_librarian(request, pk):
   """View function for renewing a specific BookInstance by librarian."""
   
   book_instance = get_object_or_404(BookInstance, pk=pk)
   
   # If this is a POST request then process the Form data
   if request.method == 'POST':
      # Create a form instance and populate it with data from the requst (binding):
      form = RenewBookForm(request.POST)
      
      # Check if the form is valid:
      if form.is_valid():
         # Process the data in form.cleaned_data as required (here we just write it to the model due_back field)
         book_instance.due_back = form.cleaned_data['renewal_date']
         book_instance.save()
         
         # redirect to a new URL:
         return HttpResponseRedirect(reverse('all-borrowed'))
      
      # If this is a GET (or any other method) create the default form.
      else:
         proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
         form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
         
      context = {
         'form': form,
         'book_instance': book_instance,
      }
      
      return render(request, 'catalog/book_renew_librarian.html', context)
   
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
   """Generic class-based view listing books on loan to current user."""
   
   model = BookInstance
   template_name = 'catalog/bookinstance_list_borrowed_user.html'
   paginate_by = 10
   
   def get_queryset(self):
      return (
         BookInstance.objects.filter(borrower = self.request.user)
         .filter(status__exact='o')
         .order_by('due_back')
      )