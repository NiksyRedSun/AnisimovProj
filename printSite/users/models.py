from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from justsite.models import Items




class User(AbstractUser):
    cart = models.ManyToManyField(Items, blank=True, related_name='items', verbose_name="Корзина")


