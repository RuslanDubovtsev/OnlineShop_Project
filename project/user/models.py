from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# from shop.models import Goods

# Create your models here.

class User(AbstractUser):
    email = models.EmailField('Email Field', unique=True)
    name = models.CharField('Name Field', max_length=50, blank=True, default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None


class Vendor(User):
    age = models.IntegerField(verbose_name='Age')
    phone = models.CharField(max_length=20, verbose_name='Phone number')
    company = models.CharField(max_length=50, verbose_name='Your Company(optional)', blank=True)

    class Meta(AbstractUser.Meta):
        verbose_name = 'Vendor'
        verbose_name_plural = ('Vendor')
        permissions = (
            ("can_see_link", "Can see the link"),
        )

class Buyer(User):
    age = models.IntegerField(verbose_name='Age')
    phone = models.CharField(max_length=20, verbose_name='Phone number')

    class Meta(AbstractUser.Meta):
        verbose_name = 'Buyer'
        verbose_name_plural = ('Buyer')


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name='name', blank=True)
    date_registration = models.DateTimeField(verbose_name='date_of_registration', auto_now_add=True)
    info = models.TextField(blank=True)
    location = models.CharField(max_length=50, verbose_name='location')
    group = models.CharField(max_length=20, verbose_name='group', blank=True)

    def __str__(self):
        return self.name

#
class Order(models.Model):
    user = models.ManyToManyField('User')
    goods = models.ManyToManyField('shop.Goods')
    address = models.CharField(max_length=100, verbose_name='Напишите ваш адрес', default='')

