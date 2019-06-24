from django.shortcuts import render, redirect, get_object_or_404
from django import views
from django.views.generic import DetailView
from django.contrib import messages

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
                           'comment_form': comment_form})


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

