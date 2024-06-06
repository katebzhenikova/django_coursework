from random import random

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from mainapp.forms import BlogForm
from mainapp.models import Blog
from newsletter.models import NewsletterSettings, Client


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('mainapp:blog_list')
    template_name = 'main/blog_form.html'

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.blog_title)
            new_blog.save()
        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('mainapp:blog_list')
    template_name = 'main/blog_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['newslettersettings_count'] = NewsletterSettings.objects.all().count()
        context_data['active_newslettersettings_count'] = NewsletterSettings.objects.filter(is_active=True).count()
        blog_list = list(Blog.objects.all())
        context_data['blog_list'] = blog_list[:3]
        context_data['clients_count'] = Client.objects.all().count()
        return context_data


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('mainapp:blog_detail')
    template_name = 'main/blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'main/blog_form.html'

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.blog_title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mainapp:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('mainapp:blog_list')
    template_name = 'main/blog_confirm_delete.html'


@login_required

def toggle_activity(request, pk):
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.blog_is_published:
        blog_item.blog_is_published = False
    else:
        blog_item.blog_is_published = True

    blog_item.save()

    return redirect(reverse('mainapp:blog_list'))



