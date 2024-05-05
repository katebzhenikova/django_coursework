from django.db import models

from config import settings

NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):
    blog_title = models.CharField(max_length=100, verbose_name='заголовок')
    slug = models.CharField(max_length=100, verbose_name='url для пользователя')
    description = models.TextField(max_length=500, verbose_name='содержимое')
    blog_image = models.ImageField(upload_to='photo_blog/', verbose_name='изображение', **NULLABLE)
    product_date = models.DateTimeField(verbose_name='дата создания', **NULLABLE)
    blog_is_published = models.BooleanField(default=True, verbose_name='опубликован')
    view_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f'{self.blog_title}'

    class Meta:
        verbose_name = 'блоговая запись'
        verbose_name_plural = 'блоговые записи'
        ordering = ('blog_title',)

