from django.shortcuts import render, redirect, get_object_or_404, reverse
from django import views
from django.views.generic import DetailView
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
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
from datetime import datetime


def index_page_view(request):

    books = Book.objects.all()
    # popular books
    popular_books = books.annotate(popular=Count('likes')).order_by('-popular')[:10]
    # book collections
    collections = Collection.objects.all()
    # book categories
    categories = Category.objects.all()

    context = {
        "books": books,
        "collections": collections,
        "categories": categories,
        "popular_books": popular_books
    }

    return render(request, "book/index.html", context=context)


# GENRES VIEW
class CategoryListView(views.generic.ListView):

    queryset = Category.objects.all()
    context_object_name = "categories"


class SubCategoryDetailView(views.generic.DetailView):

    model = SubCategory

    context_object_name = 'subcategory'


# Books VIEW
def book_detail(request, pk):
    # getting book object
    book = get_object_or_404(Book, id=pk)
    # book category
    categories = Category.objects.all()
    # book comments
    comments = book.comments.all().order_by("-created")[0:4]
    # user liked books
    if not request.user.is_anonymous:
        liked_books = request.user.book_likes.all()[:4]
    liked_books = None

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

    if request.is_ajax():
        # means comment was posted
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            user = request.user

            # we have to get user object for comment
            if user.is_anonymous:
                messages.warning(request, "Please Log In to leave comments.")
                return redirect('user-login')
            else:
                comment.user = user

            comment.book = book
            comment.body = comment_form.cleaned_data.get('body')
            comment.save()

            ajax_username = user.username
            ajax_comment_body = comment.body
            ajax_comment_date = comment.created.strftime("%B %d,%Y, %I:%M %p")

            data = {
                "username": ajax_username,
                "body": ajax_comment_body,
                "date": ajax_comment_date
            }

            return JsonResponse(data)
    else:
        comment_form = CommentForm()
    return render(request,
                  'book/product_detail.html',
                  context={'book': book,
                           'comments': comments,
                           'comment_form': comment_form,
                           'similar_books': similar_books,
                           'liked_books': liked_books,
                           'categories': categories})


def book_tag_list(request, tag_slug=None):

    object_list = Book.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    return render(request, 'book/book_list.html', context={"books": object_list,
                                                            "tag": tag})


# Like View
def book_like_view(request, pk):

    book = get_object_or_404(Book, pk=pk)
    user = request.user
    is_liked = False
    ajax = ''

    if request.is_ajax():
        if request.user in book.likes.all():
            book.likes.remove(user)
            is_liked = False
        else:
            book.likes.add(user)
            is_liked = True

        data = {
            "is_liked": is_liked,
        }
        return JsonResponse(data)
    else:
        return render(request, 'book/book_detail.html', context={"error": "error"})


# popular books
def popular_books_view(request):

    books = Book.objects.all()
    popular_books = books.annotate(popular=Count('likes')).order_by('-popular')[:10]

    return render(request, 'book/popular_books.html', context={'popular_books': popular_books})


# Collections View
class CollectionListView(views.generic.ListView):
    queryset = Collection.objects.all()
    context_object_name = "collections"


class CollectionDetailView(views.generic.DetailView):
    model = Collection

