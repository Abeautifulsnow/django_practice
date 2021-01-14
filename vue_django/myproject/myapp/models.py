from django.db import models

# Create your models here.


class Book(models.Model):
    book_name = models.CharField(max_length=64, verbose_name='book name')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='add time')

    def __str__(self):
        return self.book_name
