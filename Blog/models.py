from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify

# Create your models here.

class BlogArticles(models.Model):
    title = models.CharField(max_length=300, help_text="标题")
    author = models.ForeignKey(User, related_name="blog_posts", help_text="作者",  on_delete=models.CASCADE)
    body = models.TextField(help_text="文章")
    publish = models.DateTimeField(default=timezone.now)

    class Mate:
        ordering = ("-publish",)

    def __str__(self):
        return self.title

class ArticleColumn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    column = models.CharField(max_length=64, help_text="栏目")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.column

    
class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, related_name="article_column", on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now())
    updated = models.DateTimeField(auto_now=True)

    class Mate:
        ordering = ("title")
        index_together = (("id", 'slug'), )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("article:show_article", args=[self.id, self.slug])        