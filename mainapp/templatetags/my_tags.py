from django import template

register = template.Library()


@register.filter()
def get_image(blog):
    if blog.blog_image:
        return blog.blog_image.url
    else:
        return f'/media/photo_blog/no_photo.png'


