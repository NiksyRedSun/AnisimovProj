from django.contrib import admin
from django.urls import path, re_path, register_converter
from . import views




urlpatterns = [
    path('', views.PrintSiteHome.as_view(), name="home"), #127.0.0.1:8000
    path('about', views.AboutSite.as_view(), name="about"),
    path('contact', views.Contact.as_view(), name="contact"),
    path('item/<slug:item_slug>/', views.ShowItem.as_view(), name="item"),
    path('category/<slug:cat_slug>', views.ItemCategory.as_view(), name="category"),
    path('tag/<slug:tag_slug>/', views.ItemsTags.as_view(), name='tag'),

    path('to_cart/<slug:item_slug>/', views.to_cart, name="to_cart"),
    path('delete_from_cart/<slug:item_slug>/', views.delete_from_cart, name="delete_from_cart"),
    path('create_order/', views.create_order, name="create_order"),
    path('cart/', views.CartSummary.as_view(), name="cart"),
    path('orders/', views.Orders.as_view(), name="orders"),
]
