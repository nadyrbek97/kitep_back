from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

from . import choices


class Writer(models.Model):
    full_name = models.CharField(max_length=250)

    def __str__(self):
        return self.full_name


class Category(models.Model):
    title = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(max_length=250)
    main_genre = models.ForeignKey(Category,
                                   on_delete=models.CASCADE,
                                   related_name="subcategories")

    class Meta:
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('sub-category-detail', kwargs={'pk': self.pk})


class Collection(models.Model):
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to="collection_images")

    def __str__(self):
        return "{} ({})".format(self.title, str(self.books.count()))


class Book(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    pages = models.PositiveIntegerField(default=0,
                                        verbose_name='page')
    amount = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    language = models.CharField(max_length=20,
                                default='English',
                                choices=choices.BOOK_LANGUAGE)
    published_year = models.CharField(max_length=10)
    image = models.ImageField(upload_to="book_images",
                              default="book_images/default.png",
                              blank=True)
    file = models.FileField(upload_to="book_files",
                            null=True)
    writer = models.ForeignKey(Writer,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE,
                               related_name="books")
    sub_category = models.ManyToManyField(SubCategory,
                                          related_name="books")
    collection = models.ForeignKey(Collection,
                                   null=True,
                                   blank=True,
                                   on_delete=models.CASCADE,
                                   related_name="books")
    tags = TaggableManager()
    likes = models.ManyToManyField(User,
                                   related_name="book_likes",
                                   blank=True)

    def __str__(self):
        return self.title + "(" + self.published_year + ")"

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    book = models.ForeignKey(Book,
                             on_delete=models.CASCADE,
                             related_name="comments")
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="comments")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return "Comment by {} on {}".format(self.user.username, self.book.title)

