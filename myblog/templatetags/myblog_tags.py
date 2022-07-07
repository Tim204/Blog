from django import template
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
