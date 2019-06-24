from django import template
from django.db.models import Count
from ..models import Book

register = template.Library()

"""
    In the preceding template tag, we build a QuerySet using the
    annotate() function to aggregate the total number of comments for
    each post. We use the Count aggregation function to store the number
    of comments in the computed field total_comments for each Post object.
    We order the QuerySet by the computed field in descending order.
    We also provide an optional count variable to limit the total number
    of objects returned.
"""
@register.simple_tag
def get_most_commented_books(count=5):
    return Book.objects.annotate(
                total_comments=Count('comments'))\
               .order_by('-total_comments')[:count]
