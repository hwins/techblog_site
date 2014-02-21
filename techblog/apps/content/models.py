from django.db import models
from tinymce.models import HTMLField


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    body_primary = HTMLField()
    body_secondary = HTMLField()
    created = models.DateTimeField()
    published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(blank=True,
                                        null=True,
                                        )

    def __str__(self):
        return self.title


class Post_Topic(models.Model):
    post_id = models.ForeignKey('Post')
    topic_id = models.ForeignKey('Topic')

    class Meta:
        unique_together = (('post_id', 'topic_id'))


class Topic(models.Model):
    """categories with a null parent are top level
    however if there is a parent then they are the
    child of that parent
    """
    topic_name = models.CharField(max_length=50)
    topic_parent = models.ForeignKey('Topic',
                                     blank=True,
                                     null=True,
                                     on_delete=models.SET_NULL,
                                     )
    topic_url_format = models.CharField(max_length=50)

    class Meta:
        ordering = ['topic_name']

    def __str__(self):
        return self.topic_name
