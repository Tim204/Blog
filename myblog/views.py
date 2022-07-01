from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from .models import BlogPost


def post_list(request):
    object_list = BlogPost.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    context = {'page': page,'posts': posts}
    return render(request,
                 'myblog/post/list.html',
                 context)

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
