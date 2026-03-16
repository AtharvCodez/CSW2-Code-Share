from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Drafts'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=100,
        unique_for_date='publish'
    )

    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail_by_datewithslug',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )
    
class Comment(models.Model):
    post=models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )   
    name=models.CharField(max_length=100)
    email = models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    class Meta():
        ordering=['created']
        indexes=[models.Index(fields=['created']),
                 ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'