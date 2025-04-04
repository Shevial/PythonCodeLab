from django.db import models
from django.utils import timezone

class Post(models.Model):
    class Status(models.TextChoices):
        RAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.RAFT
)


    class Meta:
        ordering = ['-publish'] #Posts will be returned in reverse chronological order by default.
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title