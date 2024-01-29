from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from justsite.models import Items




class User(AbstractUser):
    cart = models.ManyToManyField(Items, blank=True, related_name='cart', verbose_name="Корзина", through="Cart")



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', db_constraint=False)
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='item', db_constraint=False)



