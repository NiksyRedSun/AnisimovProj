from django import template
from django.db.models import Count

from justsite.models import Category, TagItem



register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def one_digit_after_dot(num, num_dig=1):
    return format(num, f'.{num_dig}f')


@register.inclusion_tag('justsite/list_categories.html')
def show_categories(cat_selected_id=0):
    cats = Category.objects.annotate(total=Count("items")).filter(total__gt=0)
    return {"cats": cats, "cat_selected": cat_selected_id}


@register.inclusion_tag('justsite/list_tags.html')
def show_all_tags(tag_selected_id=0):
    tags = TagItem.objects.annotate(total=Count("tags")).filter(total__gt=0)
    return {"tags": tags, "tag_selected": tag_selected_id}
