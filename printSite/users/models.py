from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from justsite.models import Items




class User(AbstractUser):
    cart = models.ManyToManyField(Items, blank=True, related_name='cart', verbose_name="Корзина", through="Cart")
    phone_num = models.CharField(max_length=12, verbose_name="Номер телефона", blank=True, null=True)



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_users', db_constraint=False)
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='cart_items', db_constraint=False)



