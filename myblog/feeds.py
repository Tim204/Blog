from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import BlogPost


class LatestPostsFeed(Feed):
    """Requires opening with the URL in an RSS client
    to see the feeds in a user friendly manner
    """
    title = 'My blog'
    link = reverse_lazy('myblog:post_list')
    description = 'New posts of my blog.'

    def items(self):
        return BlogPost.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)