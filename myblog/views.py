from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from .models import BlogPost
from .forms import BlogPostEmailForm


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


def post_share(request, post_id):
    # Retrieves blog posts by id
    post = get_object_or_404(BlogPost, id=post_id, status='published')
    if request.method == 'POST':
        # Form was submitted
        form = BlogPostEmailForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
    else:
        form =  BlogPostEmailForm()
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'myblog/post/share.html', context)

