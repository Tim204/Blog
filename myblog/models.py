from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class BlogPost(models.Model):
    STATUS_CHOICE_DRAFT = 'draft'
    STATUS_CHOICE_PUBLISHED = 'published'
    STATUS_CHOICES = (
        (STATUS_CHOICE_DRAFT, 'Draft'),
        (STATUS_CHOICE_PUBLISHED, 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=STATUS_CHOICE_DRAFT)
    thumbnail = models.ImageField(upload_to='blogpost/images', blank=True)
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.
    tags = TaggableManager()

    class Meta:
        # Orders by date published from latest to earliest
        ordering = ('-publish',)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('myblog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])


class AuthorProfile(models.Model):
    
    pass



class Comment(models.Model):
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
