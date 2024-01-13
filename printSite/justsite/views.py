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

from justsite.models import Items
from justsite.utils import DataMixin


# Create your views here.


class PrintSiteHome(DataMixin, ListView):
    template_name = 'justsite/index.html'
    context_object_name = 'items'
    title_page = "Главная страница"
    cat_selected = 0


    def get_queryset(self):
        return Items.published.all().select_related('cat')