from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


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

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

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
