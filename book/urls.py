from django.urls import path
from .views import (index_page_view,
                    BookDetailView,
                    SubCategoryDetailView,
                    CategoryListView,
                    CollectionDetailView,
                    CollectionListView)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index_page_view, name='index-page-view'),
    path('categories', CategoryListView.as_view(), name='category-list'),
    path('subcategory/<int:pk>/', SubCategoryDetailView.as_view(), name='sub-category-detail'),
    # book
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    # collections
    path('collections', CollectionListView.as_view(), name='collection-list'),
    path('collection/<int:pk>/', CollectionDetailView.as_view(), name='collection-detail')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
