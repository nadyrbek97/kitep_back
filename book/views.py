from django.shortcuts import render, redirect, get_object_or_404
from django import views
from django.views.generic import DetailView
from django.contrib import messages
from django.db.models import Count
"""
        This is the Count aggregation function of the Django ORM. This
    function will allow us to perform aggregated counts of tags.
    django.db.models includes the following aggregation functions:
"""


from .models import (Book,
                     Category,
                     SubCategory,
                     Writer,
                     Collection,
                     Comment,)
from .forms import (CommentForm, )
from taggit.models import Tag


def index_page_view(request):

    books = Book.objects.all()
    collections = Collection.objects.all()
    context = {
        "books": books,
        "collections": collections,
    }

    return render(request, "book/base.html", context=context)


# GENRES VIEW
class CategoryListView(views.generic.ListView):

    queryset = Category.objects.all()
    context_object_name = "categories"


class SubCategoryDetailView(views.generic.DetailView):

    model = SubCategory

    context_object_name = 'subcategory'


# Books VIEW
def book_detail(request, pk):

    book = get_object_or_404(Book, id=pk)

    # List of all comments
    comments = book.comments.all()

    # List of similar books
    book_tag_ids = book.tags.values_list('id', flat=True)
    similar_books = Book.objects.filter(tags__in=book_tag_ids).exclude(id=book.id)
    similar_books = similar_books.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
    """
        1. We retrieve a Python list of IDs for the tags of the current
        post. The values_list() QuerySet returns tuples with the
        values for the given fields. We pass flat=True to it to get a flat
        list like [1, 2, 3, ...] .
        
        2. We get all posts that contain any of these tags, excluding the
        current post itself.
        
        3. We use the Count aggregation function to generate a
        calculated field— same_tags —that contains the number of tagsshared with all the tags queried.
        
        4. We order the result by the number of shared tags
        (descending order) and by publish to display recent posts first
        for the posts with the same number of shared tags. We slice
        the result to retrieve only the first four posts.
    """

    if request.method == "POST":
        # means comment was posted
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            user = request.user
            if user.is_anonymous:
                messages.warning(request, "Please Log In to leave comments.")
                return redirect('user-login')
            else:
                comment.user = user
            comment.book = book
            comment.body = comment_form.cleaned_data.get('body')
            comment.save()

            return redirect('book-detail', book.pk)
    else:
        comment_form = CommentForm()
    return render(request,
                  'book/book_detail.html',
                  context={'book': book,
                           'comments': comments,
                           'comment_form': comment_form,
                           'similar_books': similar_books})


def book_tag_list(request, tag_slug=None):

    object_list = Book.objects.all()

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    return render(request, 'book/book_list.html', context={ "books": object_list,
                                                            "tag": tag})


# Collections View
class CollectionListView(views.generic.ListView):
    queryset = Collection.objects.all()
    context_object_name = "collections"


class CollectionDetailView(views.generic.DetailView):
    model = Collection

