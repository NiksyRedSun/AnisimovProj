from django.contrib import messages
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
from django.db.models import F, Value
from justsite.models import Items, TagItem, Comments
from justsite.utils import DataMixin
from users.models import Cart
from django.db.models import Count, Sum, Avg, Max, Min
from .forms import AddCommentForm


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



# class ShowItem(DataMixin, DetailView):
#     model = Items
#     template_name = 'justsite/item.html'
#     slug_url_kwarg = 'item_slug'
#     context_object_name = 'item'
#     form = AddCommentForm()
#
#
#
#     def get_object(self, queryset=None):
#         self.item = get_object_or_404(Items.published, slug=self.kwargs[self.slug_url_kwarg])
#         return self.item
#
#
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return self.get_mixin_context(context, form=self.form)
#
#
#
#     def post(self, request, item_slug):
#         form = AddCommentForm(request.POST)
#
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.item = get_object_or_404(Items.published, slug=self.kwargs[self.slug_url_kwarg])
#             obj.save()
#             messages.add_message(request, messages.SUCCESS, 'Ваш комментарий сохранен')
#             return redirect('item', item_slug=item_slug)
#
#         context = self.get_context_data()
#         context['form'] = form
#         return render(self.template_name, context)


class ShowItem(DataMixin, TemplateView):
    template_name = 'justsite/item.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Обзор"
        context['item'] = get_object_or_404(Items.published, slug=self.kwargs['item_slug'])
        context['form'] = AddCommentForm()
        context['comments'] = Comments.objects.filter(item=context['item']).select_related('user')
        if self.request.user.is_authenticated:
            context['user_comment'] = context['comments'].filter(user=self.request.user).exists()

        return self.get_mixin_context(context)


    def post(self, request, item_slug):
        form = AddCommentForm(request.POST)
        item = get_object_or_404(Items.published, slug=item_slug)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.item = item
            obj.save()

            if obj.rating is not None:
                rating = Comments.objects.filter(item=item).aggregate(Avg('rating'))
                item.rate=rating['rating__avg']
                item.save()

            messages.add_message(request, messages.SUCCESS, 'Ваш комментарий сохранен')
            return redirect('item', item_slug=item_slug)

        context = self.get_context_data()
        context['form'] = form
        return render(request, 'justsite/item.html', context)




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
    try:
        item = Items.objects.get(pk=item_id)
        c = Cart(user=request.user, item=item)
        c.save()
        messages.add_message(request, messages.SUCCESS, 'Товар успешно добавлен в корзину')
        return redirect(request.META['HTTP_REFERER'])
    except:
        messages.add_message(request, messages.WARNING, 'Что-то пошло не так')

        return redirect(request.META['HTTP_REFERER'])



@login_required
def delete_from_cart(request, item_id):
    try:
        item = Cart.objects.filter(user=request.user, item__pk=item_id)[0]
        item.delete()
        messages.add_message(request, messages.SUCCESS, 'Товар удален')
        return redirect(request.META['HTTP_REFERER'])
    except Exception as e:
        print(e)
        messages.add_message(request, messages.WARNING, 'Что-то пошло не так')

        return redirect(request.META['HTTP_REFERER'])




class CartSummary(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'justsite/cart.html'
    context_object_name = 'cart_items'
    title_page = "Корзина"


    def get_queryset(self):
        q = Cart.objects.filter(user=self.request.user).select_related('items').values('item_id', 'item__price', 'item__name').annotate(Count('item_id'))
        for x in q:
            x.update({'total': x['item_id__count']*x['item__price']})

        # в данном случае расчет данных на стороне сервера приводит к уменьшению запросов на 1, второй случай - через запрос к БД
        self.summ = sum(map(lambda x: x['total'], q))
        # self.summ = q.aggregate(summ=Sum('total'))['summ']
        return q

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, summ=self.summ)

