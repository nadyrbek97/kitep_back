from django.urls import path
from .views import (index_page_view,
                    book_detail,
                    book_tag_list,
                    book_like_view,
                    SubCategoryDetailView,
                    CategoryListView,
                    CollectionDetailView,
                    CollectionListView,)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index_page_view, name='index-page-view'),
    path('categories', CategoryListView.as_view(), name='category-list'),
    path('subcategory/<int:pk>/', SubCategoryDetailView.as_view(), name='sub-category-detail'),
    # book
    path('book/<int:pk>/', book_detail, name='book-detail'),
    path('book/tag/<slug:tag_slug>', book_tag_list, name="book-tag-list"),
    # like redirect view
    # path('book/like/', BookLikeToggleView.as_view(), name="book-like-toggle"),
    path('book/like/', book_like_view, name='book-like-view'),
    # collections
    path('collections', CollectionListView.as_view(), name='collection-list'),
    path('collection/<int:pk>/', CollectionDetailView.as_view(), name='collection-detail'),
    # ajax


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
