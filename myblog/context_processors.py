from .models import BlogPost
from taggit.models import Tag


def blog(request):
    blog_post = BlogPost.objects.all()
    tags = Tag.objects.all().distinct()

    context = {
        'blog_posts': blog_post,
        'tags': tags,
        }
    return context