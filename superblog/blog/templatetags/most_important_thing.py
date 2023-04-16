from django import template
from django.db.models import *
from blog.models import Post, Author, Category

register = template.Library()

@register.inclusion_tag('blog/test_header_category.html')
def show_header_slider():
    active_category = Category.objects.annotate(cnt_post = Count('post')).filter(cnt_post__gt=0)
    return {'active_category': active_category}

@register.inclusion_tag('blog/sidebar_all_categories_tpl.html')
def show_all_categories():
    categories = Category.objects.annotate(cnt_post = Count('post__id')).filter(cnt_post__gt=0)
    return { 'categories': categories }

