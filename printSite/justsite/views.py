from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from justsite.models import Items, TagItem
from justsite.utils import DataMixin


# Create your views here.



class PrintSiteHome(DataMixin, ListView):
    template_name = 'justsite/index.html'
    context_object_name = 'items'
    title_page = "Главная страница"
    cat_selected = 0


    def get_queryset(self):
        return Items.published.all().select_related('cat')



class AboutSite(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'justsite/index.html'
    title_page = "О сайте"



class Contact(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'justsite/index.html'
    title_page = "Связаться с нами"



class ShowItem(DataMixin, DetailView):
    model = Items
    template_name = 'justsite/item.html'
    slug_url_kwarg = 'item_slug'
    context_object_name = 'item'


    def get_object(self, queryset=None):
        return get_object_or_404(Items.published, slug=self.kwargs[self.slug_url_kwarg])




class ItemCategory(DataMixin, ListView):
    template_name = 'justsite/index.html'
    context_object_name = 'items'

    allow_empty = False

    def get_queryset(self):
        return Items.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['items'][0].cat
        return self.get_mixin_context(context, title="Категория - " + cat.name, cat_selected=cat.pk)



class ItemsTags(DataMixin, ListView):
    template_name = 'justsite/index.html'
    context_object_name = 'items'
    allow_empty = False


    def get_queryset(self):
        return Items.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagItem, slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title="Тег: " + tag.tag)




@login_required
def to_cart(request, item_id):
    user = get_user_model().objects.get(pk=request.user.id)
    item = Items.objects.get(pk=item_id)
    user.cart.add(item)
    print("Опа нихуя")
    return HttpResponse()


