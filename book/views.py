from django.shortcuts import render, redirect, get_object_or_404, reverse
from django import views
from django.template.loader import render_to_string
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

    comments = book.comments.all().order_by("-created")[:4]

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

            # return redirect('book-detail', book.pk)
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

    return render(request, 'book/book_list.html', context={"books": object_list,
                                                            "tag": tag})


def book_like(request, *args, **kwargs):
    book_id = request.POST.get('book_id')
    action = request.POST.get('data-action')
    if book_id and action:
        try:
            book = book_id.objects.get(id=book_id)
            if action == 'like':
                book.likes.add(request.user)
            else:
                book.likes.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    print(book_id)
    print(action)
    return JsonResponse({'status':'ko'})


# Like View
def book_like_view(request, pk):

    book = get_object_or_404(Book, pk=pk)
    user = request.user
    is_liked = False
    ajax = ''

    if request.is_ajax():
        ajax += " is ajax"
        if request.user in book.likes.all():
            book.likes.remove(user)
            is_liked = False
            print("user removed")
        else:
            print("user added")
            book.likes.add(user)
            is_liked = True

        data = {
            "is_liked": is_liked,
            "is_ajax": ajax
        }
        print(data)
        return JsonResponse(data)
    else:
        return render(request, 'book/book_detail.html', context={"error": "error"})

# class BookLikeToggleView(views.genec.RedirectView):
#     permanent = False
#     query_string = True
#     pattern_name = "book-detail"
#
#     def get_redirect_url(self, *args, book_id=None, **kwargs):
#
#
#         print(kwargs)
#         pk = get_object_or_404(Book, id=self.request.POST.get("data-id"))
#         book = get_object_or_404(Book, pk=pk)
#         # getting url for redirecting to the same page
#         url_ = book.get_absolute_url()
#         user = self.request.user
#
#         if user.is_authenticated():
#             if user in book.likes.all():
#                 book.likes.remove(user)
#             else:
#                 book.likes.add(user)
#
#         return super().get_redirect_url(*args, **kwargs)


# Collections View
class CollectionListView(views.generic.ListView):
    queryset = Collection.objects.all()
    context_object_name = "collections"


class CollectionDetailView(views.generic.DetailView):
    model = Collection

