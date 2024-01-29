from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.db.models import F, Value
from django.template.defaultfilters import slugify
from django.urls import reverse




class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Items.Status.PUBLISHED)


class Items(models.Model):

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    name = models.CharField(max_length=255, verbose_name="Название товара")
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name="Слаг", validators=[
        MinLengthValidator(5, message="Минимум 5 символов"),
        MaxLengthValidator(100, message="Максимум 100 символов"),
    ])
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Фото")
    description = models.TextField(blank=True, verbose_name="Описание")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Статус")
    cat = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name='items', verbose_name="Категория", null=True)
    tags = models.ManyToManyField('TagItem', blank=True, related_name='tags', verbose_name="Теги")
    price = models.IntegerField(blank=True, verbose_name="Цена", null=True)
    rate = models.FloatField(blank=True, verbose_name="Рейтинг", null=True)

    published = PublishedModel()

    objects = models.Manager()


    def __str__(self):
        return self.name


    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]
        verbose_name = "Товары магазина"
        verbose_name_plural = 'Товары магазина'



    def get_absolute_url(self):
        return reverse('item', kwargs={'item_slug': self.slug})




class Comments(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments', db_constraint=False)
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='comments', db_constraint=False)
    text = models.TextField(blank=True, verbose_name="Текст комментария", null=True)
    rating = models.IntegerField(blank=True, verbose_name="Оценка:", null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")


    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]
        verbose_name = "Комментарий"
        verbose_name_plural = 'Комментарии'


class Order(models.Model):

    class Status(models.IntegerChoices):
        ONTHEJOB = 0, 'В работе'
        READYTOGO = 1, 'Готов к выдаче'
        FINISHED = 2, 'Выдан'


    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_orders')
    item = models.ManyToManyField(Items, related_name='order_item')

    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    status = models.IntegerField(choices=Status.choices, default=Status.ONTHEJOB)
    order_sum = models.IntegerField(blank=True, verbose_name="Стоимость заказа", null=True)



    class Meta:
        ordering = ['time_create']
        indexes = [
            models.Index(fields=['time_create']),
        ]
        verbose_name = "Заказ"
        verbose_name_plural = 'Заказы'



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='items')
    count = models.IntegerField(blank=True, verbose_name="Количество товара", null=True)



class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'




class TagItem(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


