from django.shortcuts import get_object_or_404, render
from .models import BlogPost


def post_list(request):
    posts = BlogPost.published.all()
    context = { 'posts': posts}
    return render(
        request, 
        'myblog/post/list.html',
        context
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(BlogPost, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    context = {'post': post}
    return render(request,
                  'myblog/post/detail.html',
                  context
                  )
