from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from .models import BlogPost


class PostListView(ListView):
    queryset = BlogPost.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'myblog/post/list.html'


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
