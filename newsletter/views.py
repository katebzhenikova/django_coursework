import random

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from mainapp.models import Blog
from newsletter.forms import ClientForm, NewsletterMessageForm, NewsletterSettingsForm, NewsletterSettingsModerationForm
from newsletter.models import Client, NewsletterMessage, NewsletterSettings, NewsletterLog


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mainapp:client_list')
    template_name = 'newsletter/client_form.html'

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save()
            new_client.save()
        return super().form_valid(form)



class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')
    template_name = 'newsletter/client_form.html'

    def get_form_class(self):
        return super().get_form_class()

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


class ClientListView(ListView):
    model = Client
    template_name = 'newsletter/client_list.html'


class ClientDetailView(DetailView):
    model = Client
    form_class = ClientForm
    template_name = 'newsletter/client_form.html'

    def get_form_class(self):
        return super().get_form_class()


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('newsletter:client_list')
    template_name = 'newsletter/client_confirm_delete.html'
    permission_required = 'newsletter.delete_client'


class NewsletterMessageCreateView(CreateView):
    model = NewsletterMessage
    form_class = NewsletterMessageForm
    success_url = reverse_lazy('newsletter:newslettermessage_list')
    template_name = 'newsletter/newsletter_form.html'

    def form_valid(self, form):
        if form.is_valid():
            new_newslettermessage = form.save()
            new_newslettermessage.save()
        return super().form_valid(form)


class NewsletterMessageUpdateView(UpdateView):
    model = NewsletterMessage
    form_class = NewsletterMessageForm
    success_url = reverse_lazy('newsletter:newslettermessage_list')
    template_name = 'newsletter/newsletter_form.html'

    def get_form_class(self):
        return super().get_form_class()


class NewsletterMessageListView(ListView):
    model = NewsletterMessage
    template_name = 'newsletter/newsletter_list.html'


class NewsletterMessageDetailView(DetailView):
    model = NewsletterMessage
    template_name = 'newsletter/newsletter_page.html'
    fields = '__all__'


class NewsletterMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = NewsletterMessage
    form_class = NewsletterMessageForm
    success_url = reverse_lazy('newsletter:newslettermessage_list')
    template_name = 'newsletter/newsletter_confirm_delete.html'
    permission_required = 'newsletter.delete_newslettermessage'

    def get_form_class(self):
        return super().get_form_class()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        return context


class NewsletterSettingsCreateView(CreateView):
    model = NewsletterSettings
    form_class = NewsletterSettingsForm
    success_url = reverse_lazy('newsletter:mail_list')
    template_name = 'newsletter/mail_form.html'

    def form_valid(self, form):
        if form.is_valid():
            new_newslettermessage = form.save()
            new_newslettermessage.save()
        return super().form_valid(form)


class NewsletterSettingsUpdateView(UpdateView):
    model = NewsletterSettings
    form_class = NewsletterSettingsForm
    success_url = reverse_lazy('newsletter:mail_list')
    template_name = 'newsletter/mail_form.html'

    def get_form_class(self):
        return super().get_form_class()


class NewsletterSettingsListView(ListView):
    model = NewsletterSettings
    template_name = 'newsletter/mail_list.html'


class NewsletterSettingsDetailView(DetailView):
    model = NewsletterSettings
    form_class = NewsletterSettingsForm
    template_name = 'newsletter/mail_page.html'


class NewsletterSettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = NewsletterSettings
    success_url = reverse_lazy('newsletter:mail_list')
    template_name = 'newsletter/newsletter_confirm_delete.html'
    permission_required = 'newsletter.delete_newslettermessage'

    def get_form_class(self):
        return super().get_form_class()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        return context


class NewsletterLogView(LoginRequiredMixin, ListView):
    model = NewsletterLog
    template_name = 'main/newsletterLog_list.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        newsletterlog = NewsletterLog.objects.all()
        context_data['newsletterlog'] = newsletterlog
        return context_data


class NewsletterSettingsModerationView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = NewsletterSettings
    form_class = NewsletterSettingsModerationForm
    template_name = 'main/mail_form.html'
    permission_required = ('main.set_active',)

    def get_success_url(self):
        return reverse_lazy('main:sending_detail', kwargs={'pk': self.object.pk})


# def get_context_data(request):
#     # Получить общее количество рассылок
#     newslettersettings_count = NewsletterSettings.objects.count()
#
#     # Получить количество активных рассылок
#     active_newslettersettings_count = NewsletterSettings.objects.filter(status='running').count()
#
#     # Получить количество клиентов сервиса
#     clients_count = Client.objects.count()
#
#     context = {
#         'newslettersettings_count': newslettersettings_count,
#         'active_newslettersettings_count': active_newslettersettings_count,
#         'clients_count': clients_count,
#     }
#
#     return render(request, 'blog_list.html', context)

class HomepageView(ListView):
    model = NewsletterSettings
    template_name = 'mainapp/main/blog_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['newslettersettings_count'] = NewsletterSettings.objects.all().count()
        context_data['active_newslettersettings_count'] = NewsletterSettings.objects.filter(is_active=True).count()
        blog_list = list(Blog.objects.all())
        random.shuffle(blog_list)
        context_data['blog_list'] = blog_list[:3]
        context_data['clients_count'] = Client.objects.all().count()
        return context_data

