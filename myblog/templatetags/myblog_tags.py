from django import template
from ..models import BlogPost

register = template.Library()

@register.simple_tag
def total_posts(): # Django uses the function'sname as the tag name
    return BlogPost.published.count()