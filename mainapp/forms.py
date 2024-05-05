from django import forms

from mainapp.models import Blog


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class BlogForm(forms.ModelForm, StyleFormMixin):
    class Meta:
        model = Blog
        fields = '__all__'
        # fields = ('product_name', 'description', 'product_price', 'product_image',)
        #exclude = ('product_user', )

