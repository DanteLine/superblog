from django.db import models
from pytils.translit import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
from captcha.fields import CaptchaField


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class MyTag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, verbose_name='Urlslug', unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    author_photo = models.ImageField(verbose_name='Фото', upload_to='author_photos/%Y/%m/%d/')
    about = models.TextField(verbose_name='Об авторе', max_length=999)
    slug = models.SlugField(max_length=99, unique=True, blank=True)

    def __str__(self):
            return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('author', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        first_last_name = self.first_name + ' ' + self.last_name
        self.slug = slugify(first_last_name)
        super().save(*args, **kwargs)
        img = Image.open(self.author_photo.path)
        width, height = img.size  # Get dimensions

        if width > 300 and height > 300:
            # keep ratio but shrink down
            img.thumbnail((width, height))

        # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 300 and height > 300:
            img.thumbnail((300, 300))

        img.save(self.author_photo.path)


    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

class PostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    context = models.CharField(max_length=255)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    content = models.TextField()
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    views = models.PositiveIntegerField(default=0, verbose_name='Количесво просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(MyTag)
    tags_str = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=100, verbose_name='Urlslug', unique=True, blank=True)
    captcha = CaptchaField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def add_tags(self):
        self.tags.clear()
        for i in self.tags_str.split(','):
            obj, created = MyTag.objects.get_or_create(title=i.strip().lower())
            self.tags.add(obj)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']





