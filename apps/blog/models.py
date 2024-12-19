from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from apps.authentication.models import CustomUser


class Category(MPTTModel):
    title = models.CharField(max_length=255)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to="blogs/")
    description = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="blogs")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="blogs")
    tags = models.ManyToManyField(Tag, related_name="blogs", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Menu(models.Model):
    title = models.CharField(max_length=255)
    seat_number = models.PositiveIntegerField()
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True
    )
    link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['seat_number']

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.blog.title}'

    class Meta:
        ordering = ['-id']
