from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import Item, OrderItem, Order, Payment
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from portfolio.models import Address
from django.db.models import Q, query
from functools import reduce
from operator import and_
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class IndexView(View):
    def get(self, request, *args, **kwargs):
        item_data = Item.objects.order_by('-id')
        paginator = Paginator(item_data, 8)
        page = request.GET.get('page')
        item_data = paginator.get_page(page)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render(request, 'app/index.html', {
            'item_data': item_data,
            'page_obj': page_obj
        })

class ItemDetailView(View):
    def get(self, request, *args, **kwargs):
        item_data = Item.objects.get(slug=self.kwargs['slug'])
        return render(request, 'app/product.html', {
            'item_data': item_data
        })

@login_required
def addItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
    )
    order = Order.objects.filter(user=request.user, ordered=False)

    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        order = Order.objects.create(user=request.user, ordered_data=timezone.now())
        order.items.add(order_item)

    return redirect('order')

class OrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'order': order
            }
            return render(request, 'app/order.html',context)
        except ObjectDoesNotExist:
            return render(request, 'app/order.html')

@login_required
def removeItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            return redirect('order')

        return redirect('app_prodcut', slug=slug)

@login_required
def removeSingleItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.item.remove(order_item)
                order_item.delete()
            return redirect('order')
        return redirect('app_product', slug=slug)

class PaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        user_data = User.objects.get(id=request.user.id)
        address_data = Address.objects.get(author=request.user)
        context = {
            'order': order,
            'user_data': user_data,
            'address_data': address_data,
        }
        return render(request, 'app/payment.html', context)

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        order_items = order.items.all()
        amount = order.get_total()

        payment = Payment(user=request.user)
        payment.stripe_charge_id = 'test_stripe_charge_id'
        payment.amount = amount
        payment.save()

        order_items.update(ordered=True)
        for item in order_items:
            item.save()
        address_data = Address.objects.get(author=request.user)
        order.ordered = True
        order.payment = payment
        order.name = address_data.name
        order.postal = address_data.postal
        order.address = address_data.address
        order.phone = address_data.phone
        order.save()
        return redirect('thanks')


class ThanksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/thanks.html')

class SearchView(View):
    def get(self, request, *args, **kwargs):
        item_data = Item.objects.order_by('-id')
        keyword = request.GET.get('keyword')

        if keyword:
            exclusion_list = set([' ',' '])
            query_list = ''
            for word in keyword:
                if not word in exclusion_list:
                    query_list += word
            query = reduce(and_, [Q(title__icontains=q) | Q(title__icontains=q) for q in query_list])
            item_data = item_data.filter(query)

        paginator = Paginator(item_data, 8)
        page = request.GET.get('page')
        item_data = paginator.get_page(page)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render(request, 'app/index.html', {
            'keyword': keyword,
            'item_data': item_data,
            'page_obj': page_obj
        })