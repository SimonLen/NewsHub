from django.db import models
from django.contrib.auth.models import User
from news.resources import POST_TYPES


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_of_articles_by_author = Post.post_set.all().aggregate(Sum('_rating'))['_rating__sum'] * 3
        rating_of_comments_by_author = Comment.comment_set.all().aggregate(Sum('_rating'))['_rating__sum']
        rating_of_comments_under_posts_of_author = \
            Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']

        self._rating = rating_of_comments_by_author + rating_of_comments_under_posts_of_author + \
                       rating_of_articles_by_author
        self.save()


class Category(models.Model):
    theme = models.CharField(max_length=50, unique=True)


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
