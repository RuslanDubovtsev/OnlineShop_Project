from django.db import models
from user.models import User
# Create your models here.


class Rubric(models.Model):
    rubric_title = models.CharField(max_length=50, verbose_name='rubric')

    def __str__(self):
        return self.rubric_title


class Goods(models.Model):
    title = models.CharField(max_length=50, verbose_name='title')
    short_information = models.CharField(max_length=50, verbose_name='short_information')
    information = models.TextField(verbose_name='information')
    cost = models.FloatField(verbose_name='cost')
    date = models.DateTimeField(auto_now_add=True, verbose_name='date_of_new')
    rubric = models.ForeignKey('Rubric', on_delete=models.PROTECT, verbose_name='rubric', default=1)
    photo_good = models.ImageField(upload_to='images/', default='default.jpg')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="created_by", null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=20, verbose_name='name')
    text = models.TextField()
    date_comment = models.DateTimeField(auto_now_add=True, verbose_name='date_of_new')
    goods = models.ForeignKey(Goods, on_delete=models.PROTECT, verbose_name='goods')

    def __str__(self):
        return self.name

