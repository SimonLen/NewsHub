from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache
from .resources import POST_TYPES


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _rating = models.IntegerField(default=0)

    def update_rating(self):  # the total rating consists of three components: r1, r2, r3
        r1 = self.post_set.all().aggregate(Sum('_rating'))['_rating__sum'] * 3
        # the total rating of each author's article is multiplied by 3

        r2 = self.user.comment_set.all().aggregate(Sum('_rating'))['_rating__sum']
        # the total rating of all the author's comments

        r3 = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('_rating'))['_rating__sum']
        # the total rating of all comments to the author's articles

        self._rating = r1 + r2 + r3
        self.save()

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    theme = models.CharField(max_length=50, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return f'{self.theme}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=POST_TYPES)
    creation_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    _rating = models.IntegerField(default=0, db_column='rating')

    def like(self):
        self._rating += 1
        self.save()

    def dislike(self):
        self._rating -= 1 if self._rating > 0 else 0
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    _rating = models.IntegerField(default=0, db_column='rating')

    def like(self):
        self._rating += 1
        self.save()

    def dislike(self):
        self._rating -= 1 if self._rating > 0 else 0
        self.save()
