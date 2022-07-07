from django import template
from django.db.models import Count
from ..models import BlogPost

register = template.Library()


@register.simple_tag
def total_posts():  # Django uses the function'sname as the tag name
    return BlogPost.published.count()


@register.inclusion_tag('myblog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = BlogPost.published.order_by('-publish')[:count]
    context = {'latest_posts': latest_posts}
    return context


@register.simple_tag
def get_most_commented_posts(count=5):
    return BlogPost.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]
    