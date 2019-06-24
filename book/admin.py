from django.contrib import admin
from .models import (Book,
                     Category,
                     SubCategory,
                     Writer,
                     Collection,
                     Comment)

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Writer)
admin.site.register(Collection)


class CollectionAdmin(admin.ModelAdmin):

    model = Collection


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'created')
    list_filter = ('created', )
    search_fields = ('body', )
