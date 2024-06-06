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
        # fields = '__all__'
        fields = ('blog_title', 'description', 'blog_image', 'blog_date', 'blog_is_published')
        #exclude = ('product_user', )

