from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage,\
    PageNotAnInteger
from django.core.mail import send_mail
from taggit.models import Tag
from .models import BlogPost, Comment
from .forms import BlogPostEmailForm, CommentForm


def post_list(request, tag_slug=None):
    object_list = BlogPost.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

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
        
    context = {'page': page,
               'posts': posts,
               'tag': tag
               }
    return render(request,
                 'myblog/post/list.html',
                 context,
                 )




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

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {'post': post,
               'comments': comments,
               'new_comment': new_comment,
               'comment_form': comment_form, 
               }
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
        form = BlogPostEmailForm()
    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }
    return render(request, 'myblog/post/share.html', context)
