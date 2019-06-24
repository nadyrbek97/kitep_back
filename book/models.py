from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


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
    genre = models.ManyToManyField(SubCategory,
                                   related_name="books")
    collection = models.ForeignKey(Collection,
                                   null=True,
                                   blank=True,
                                   on_delete=models.CASCADE,
                                   related_name="books")

    def __str__(self):
        return self.title + "(" + self.published_year + ")"

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})
