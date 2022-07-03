from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.core.mail import send_mail
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
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = BlogPostEmailForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form =  BlogPostEmailForm()
    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }
    return render(request, 'myblog/post/share.html', context)

