import json

from django import forms

from newsletter.models import Client, NewsletterMessage, NewsletterSettings


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(forms.ModelForm, StyleFormMixin):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('owner',)


class NewsletterMessageForm(forms.ModelForm, StyleFormMixin):
    class Meta:
        model = NewsletterMessage
        fields = '__all__'
        exclude = ('owner',)


class NewsletterSettingsForm(forms.ModelForm, StyleFormMixin):
    class Meta:
        model = NewsletterSettings
        fields = '__all__'
        exclude = ('owner',)


class NewsletterSettingsModerationForm(NewsletterSettingsForm):
    class Meta:
        model = NewsletterSettings
        fields = '__all__'

