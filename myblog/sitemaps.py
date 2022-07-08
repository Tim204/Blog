from django.contrib.sitemaps import Sitemap
from .models import BlogPost

class BlogPostSitemap(Sitemap):
    changefreq = 'weekly' # The change in frequency in post pages
    priority = 0.9 # indicates the relevance of said pages in the website

    def items(self):
        # Returns a queryset of objects included in this sitemap
        return BlogPost.published.all()
    
    def lastmod(self, obj):
        # Recieves each object returned by items() and returns the
        # last time the object was modified
        return obj.updated