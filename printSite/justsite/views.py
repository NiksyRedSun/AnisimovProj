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
from justsite.models import Items, TagItem, Comments, Order, OrderItem
from justsite.utils import DataMixin
from users.models import Cart
from django.db.models import Count, Sum, Avg, Max, Min
from .forms import AddCommentForm
from decimal import Decimal


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
def to_cart(request, item_slug):
    try:
        item = Items.objects.get(slug=item_slug)
        c = Cart(user=request.user, item=item)
        c.save()
        messages.add_message(request, messages.SUCCESS, 'Товар успешно добавлен в корзину')
        return redirect(request.META['HTTP_REFERER'])
    except Exception as e:
        print(e)
        messages.add_message(request, messages.WARNING, 'Что-то пошло не так')

        return redirect(request.META['HTTP_REFERER'])



@login_required
def delete_from_cart(request, item_slug):
    try:
        item = Cart.objects.filter(user=request.user, item__slug=item_slug)[0]
        item.delete()
        messages.add_message(request, messages.SUCCESS, 'Товар успешно удален')
        return redirect(request.META['HTTP_REFERER'])
    except Exception as e:
        print(e)
        messages.add_message(request, messages.WARNING, 'Что-то пошло не так')

        return redirect(request.META['HTTP_REFERER'])


@login_required
def create_order(request):
    try:
        q = request.user.cart.all().annotate(count=Count('id'), total=F('price')*F('count'))
        summ = sum(map(lambda x: x.total, q))
        if summ <= 0:
            messages.add_message(request, messages.WARNING, 'Ваш заказ пустой')
            return redirect(request.META['HTTP_REFERER'])

        order = Order(user=request.user, order_sum=summ)
        order.save()
        for i in q:
            OrderItem(order=order, item=i, count=i.count).save()
        Cart.objects.filter(user=request.user).delete()

        messages.add_message(request, messages.WARNING, 'Ваш заказ успешно сформирован')
        return redirect(request.META['HTTP_REFERER'])

    except Exception as e:
        print(e)
        messages.add_message(request, messages.WARNING, 'Что-то пошло не так')

        return redirect(request.META['HTTP_REFERER'])


@login_required
def delete_order(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        order.delete()
        messages.add_message(request, messages.SUCCESS, 'Заказ успешно отменен')
        return redirect(request.META['HTTP_REFERER'])

    except Exception as e:
        print(e)
        messages.add_message(request, messages.WARNING, 'Что-то пошло не так')

        return redirect(request.META['HTTP_REFERER'])


class Orders(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'justsite/orders.html'
    context_object_name = 'orders'
    title_page = "Заказы"


    def get_queryset(self):
        self.orders = self.request.user.user_orders.all()
        self.orders_items = {}
        for order in self.orders:
            res = OrderItem.objects.filter(order=order).annotate(total=F('item__price')*F('count')).values('item__name', 'count', 'total')
            self.orders_items[order] = list(res)
            print(order.__dict__)

        return self.orders


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, orders_items=self.orders_items)




class CartSummary(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'justsite/cart.html'
    context_object_name = 'cart_items'
    title_page = "Корзина"


    def get_queryset(self):
        q = self.request.user.cart.all().annotate(count=Count('id'), total=F('price')*F('count')).values('name', 'count', 'total', 'slug')
        self.summ = sum(map(lambda x: x['total'], q))
        return q

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, summ=self.summ)

