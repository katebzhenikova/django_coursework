import random

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Permission
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from mainapp.models import Blog
from newsletter.forms import ClientForm, NewsletterMessageForm, NewsletterSettingsForm, NewsletterSettingsModerationForm
from newsletter.models import Client, NewsletterMessage, NewsletterSettings, NewsletterLog


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')
    template_name = 'newsletter/client_form.html'

    def form_valid(self, form):
        newsletter_settings = form.save(commit=False)  # Сохраняем форму без коммита в базу данных
        newsletter_settings.owner = self.request.user  # Устанавливаем владельца рассылки равным текущему пользователю
        newsletter_settings.save()  # Сохраняем изменения в базу данных
        return super().form_valid(form)



class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')
    template_name = 'newsletter/client_form.html'

    def get_form_class(self):
        return super().get_form_class()

    def test_func(self):
        owner = self.request.user
        if owner == self.request.user:
            return True
        return self.handle_no_permission()

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     FormSet = inlineformset_factory(self.model, NewsletterMessage, form=NewsletterMessageForm, extra=1)
    #     if self.request.method == 'POST':
    #         formset = FormSet(self.request.POST, instance=self.object)
    #     else:
    #         formset = FormSet(instance=self.object)
    #     context_data['formset'] = formset
    #     return context_data
    #
    # def form_valid(self, form):
    #     context_data = self.get_context_data()
    #     formset = context_data['formset']
    #     with transaction.atomic():
    #         if form.is_valid():
    #             self.object = form.save()
    #             if formset.is_valid():
    #                 formset.instance = self.object
    #                 formset.save()
    #
    #     return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'newsletter/client_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    form_class = ClientForm
    template_name = 'newsletter/client_form.html'

    def get_form_class(self):
        return super().get_form_class()

    def test_func(self):
        owner = self.request.user
        if owner == self.request.user:
            return True
        return self.handle_no_permission()


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('newsletter:client_list')
    template_name = 'newsletter/client_confirm_delete.html'
    permission_required = 'newsletter.delete_client'

    def test_func(self):
        owner = self.request.user
        if owner == self.request.user:
            return True
        return self.handle_no_permission()


class NewsletterMessageCreateView(LoginRequiredMixin, CreateView):
    model = NewsletterMessage
    form_class = NewsletterMessageForm
    success_url = reverse_lazy('newsletter:newslettermessage_list')
    template_name = 'newsletter/newsletter_form.html'

    def form_valid(self, form):
        newsletter_settings = form.save(commit=False)  # Сохраняем форму без коммита в базу данных
        newsletter_settings.owner = self.request.user  # Устанавливаем владельца рассылки равным текущему пользователю
        newsletter_settings.save()  # Сохраняем изменения в базу данных
        return super().form_valid(form)




class NewsletterMessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = NewsletterMessage
    form_class = NewsletterMessageForm
    success_url = reverse_lazy('newsletter:newslettermessage_list')
    template_name = 'newsletter/newsletter_form.html'

    def get_form_class(self):
        return super().get_form_class()

    def test_func(self):
        owner = self.request.user
        if owner == self.request.user:
            return True
        return self.handle_no_permission()


class NewsletterMessageListView(LoginRequiredMixin, ListView):
    model = NewsletterMessage
    template_name = 'newsletter/newsletter_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)



class NewsletterMessageDetailView(LoginRequiredMixin, DetailView):
    model = NewsletterMessage
    template_name = 'newsletter/newsletter_page.html'
    fields = '__all__'


class NewsletterMessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = NewsletterMessage
    form_class = NewsletterMessageForm
    success_url = reverse_lazy('newsletter:newslettermessage_list')
    template_name = 'newsletter/newsletter_confirm_delete.html'

    def get_form_class(self):
        return super().get_form_class()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        return context

    def test_func(self):
        owner = self.request.user
        if owner == self.request.user:
            return True
        return self.handle_no_permission()


class NewsletterSettingsCreateView(LoginRequiredMixin, CreateView):
    model = NewsletterSettings
    form_class = NewsletterSettingsForm
    success_url = reverse_lazy('newsletter:mail_list')
    template_name = 'newsletter/mail_form.html'

    def get_form(self, form_class=None):
        form = super(NewsletterSettingsCreateView, self).get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(owner=self.request.user)
        form.fields['message'].queryset = NewsletterMessage.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(NewsletterSettingsCreateView, self).form_valid(form)

class NewsletterSettingsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = NewsletterSettings
    form_class = NewsletterSettingsForm
    success_url = reverse_lazy('newsletter:mail_list')
    template_name = 'newsletter/mail_form.html'

    def get_form_class(self):
        return super().get_form_class()

    def test_func(self):
        owner = self.request.user
        if owner == self.request.user:
            return True
        return self.handle_no_permission()


class NewsletterSettingsListView(LoginRequiredMixin, ListView):
    model = NewsletterSettings
    template_name = 'newsletter/mail_list.html'
    def get_form_class(self):
        return super().get_form_class()

    def get_queryset(self):
        if self.request.user.has_perm('newslettersettings.view_newslettersettings'):
            return super().get_queryset()
        return super().get_queryset().filter(owner=self.request.user)



class NewsletterSettingsDetailView(LoginRequiredMixin, DetailView):
    model = NewsletterSettings
    form_class = NewsletterSettingsForm
    template_name = 'newsletter/mail_page.html'

    def get_form_class(self):
        return super().get_form_class()


class NewsletterSettingsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = NewsletterSettings
    success_url = reverse_lazy('newsletter:mail_list')
    template_name = 'newsletter/newsletter_confirm_delete.html'

    def get_form_class(self):
        return super().get_form_class()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        return context

    def test_func(self):
        owner = self.request.user
        if owner == self.request.user:
            return True
        return self.handle_no_permission()


class NewsletterLogListView(LoginRequiredMixin, ListView):
    model = NewsletterLog
    template_name = 'newsletter/log_list.html'

    def get_queryset(self):
        return super().get_queryset()




