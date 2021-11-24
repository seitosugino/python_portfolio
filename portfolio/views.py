from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Post, Category, Address
from .forms import PostForm, AddressForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, query
from functools import reduce
from operator import and_
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class IndexView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        paginator = Paginator(post_data, 4)
        page = request.GET.get('page')
        post_data = paginator.get_page(page)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'portfolio/index.html', {
            'post_data': post_data,
            'page_obj': page_obj
        })

class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'portfolio/post_detail.html', {
            'post_data': post_data
        })

class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        return render(request, 'portfolio/post_form.html', {
            'form': form
        })
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            post_data.category = category_data
            post_data.content = form.cleaned_data['content']
            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
            return redirect('post_detail', post_data.id)

        return render(request, 'portfolio/post_form.html', {
            'form': form
        })

class PostEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(
            request.POST or None,
            initial = {
                'title': post_data.title,
                'category': post_data.category,
                'content': post_data.content,
                'image': post_data.image
            }
        )

        return render(request, 'portfolio/post_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            post_data.category = category_data
            post_data.content = form.cleaned_data['content']
            if request.FILES:
                post_data.image = request.FILES.get('image')
            post_data.save()
            return redirect('post_detail', self.kwargs['pk'])

        return render(request, 'portfolio/post_form.html', {
            'form': form
        })

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'portfolio/post_delete.html', {
            'post_data': post_data
        })

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('index')

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        category_data = Category.objects.get(name=self.kwargs['category'])
        post_data = Post.objects.order_by('-id').filter(category=category_data)
        return render(request, 'portfolio/index.html', {
            'post_data': post_data
        })

class SearchView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        keyword = request.GET.get('keyword')

        if keyword:
            exclusion_list = set([' ', ' '])
            query_list = ''
            for word in keyword:
                query_list += word
            query = reduce(and_, [Q(title__icontains=q) | Q(content__icontains=q) for q in query_list])
            post_data = post_data.filter(query)

        paginator = Paginator(post_data, 4)
        page = request.GET.get('page')
        post_data = paginator.get_page(page)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render(request, 'portfolio/index.html', {
            'keyword': keyword,
            'post_data': post_data,
            'page_obj': page_obj
        })

class AddressCreateView(View):
    def get(self, request, *args, **kwargs):
        form = AddressForm(request.POST or None)
        return render(request, 'portfolio/address.html', {
            'form': form
        })

class AddressEditView(View):
    def get(self, request, *args, **kwargs):
        address_data = Address.objects.get(author=request.user)
        form = AddressForm(
            request.POST or None,
            initial = {
                'name': address_data.name,
                'postal': address_data.postal,
                'address': address_data.address,
                'phone': address_data.phone,
                'description': address_data.description,
                'image': address_data.image
            }
        )
        return render(request, 'portfolio/address.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        if Address.objects.filter(author=request.user).count is None:
            form = AddressForm(request.POST or None)
            address_data = Address.objects.filter(author=request.user)
            if form.is_valid():
                address_data = Address()
                address_data.author = request.user
                address_data.name = form.cleaned_data['name']
                address_data.postal = form.cleaned_data['postal']
                address_data.address = form.cleaned_data['address']
                address_data.phone = form.cleaned_data['phone']
                address_data.description = form.cleaned_data['description']
                if request.FILES.get('image'):
                    address_data.image = request.FILES.get('image')
                address_data.save()
                return redirect('address')

            return render(request, 'portfolio/address.html', {
                'form': form
            })
        else:
            form = AddressForm(request.POST or None)
            address_data = Address.objects.get(author=request.user)
            if form.is_valid():
                address_data = Address.objects.get(author=request.user)
                address_data.author = request.user
                address_data.name = form.cleaned_data['name']
                address_data.postal = form.cleaned_data['postal']
                address_data.address = form.cleaned_data['address']
                address_data.phone = form.cleaned_data['phone']
                address_data.save()
                return redirect('address')

            return render(request, 'portfolio/address.html', {
                'form': form
            })