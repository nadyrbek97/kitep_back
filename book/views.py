from django.shortcuts import render, redirect
from django import views
from django.views.generic import DetailView
from django.contrib import messages

from .models import (Book,
                     Category,
                     SubCategory,
                     Writer,
                     Collection
                     )


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
class BookDetailView(views.generic.DetailView):

    model = Book


# Collections View
class CollectionListView(views.generic.ListView):
    queryset = Collection.objects.all()
    context_object_name = "collections"


class CollectionDetailView(views.generic.DetailView):
    model = Collection
