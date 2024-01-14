from django import template
from django.db.models import Count

from justsite.models import Category, TagItem
from justsite.utils import menu


register = template.Library()



@register.simple_tag
def get_menu():
    return menu


@register.inclusion_tag('justsite/list_categories.html')
def show_categories(cat_selected_id=0):
    cats = Category.objects.annotate(total=Count("items")).filter(total__gt=0)
    return {"cats": cats, "cat_selected": cat_selected_id}



@register.inclusion_tag('justsite/list_tags.html')
def show_all_tags():
    return {"tags": TagItem.objects.annotate(total=Count("tags")).filter(total__gt=0)}
