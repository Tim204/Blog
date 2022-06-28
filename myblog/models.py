from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class BlogPost(models.Model):
    STATUS_CHOICE_DRAFT = 'D'
    STATUS_CHOICE_PUBLISHED = 'P'
    STATUS_CHOICES = [
        (STATUS_CHOICE_DRAFT, 'Draft'),
        (STATUS_CHOICE_PUBLISHED, 'Published'),
    ]

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
    
    class Meta:
        ordering = ('-publish',) # Orders by date published from latest to earliest
    
    def __str__(self) -> str:
        return self.title
