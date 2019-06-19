from django.contrib import admin
from .models import (Book,
                     Category,
                     SubCategory,
                     Writer,
                     Collection)

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Writer)
admin.site.register(Collection)


class CollectionAdmin(admin.ModelAdmin):

    model = Collection

