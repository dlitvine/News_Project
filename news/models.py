# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    EXPERT = 'EX'
    SPECIALIST = 'SP'
    ASSOCIATE = 'AS'
    AUTHOR_OPTIONS = [
        (EXPERT, 'Expert'),
        (SPECIALIST, 'Specialist'),
        (ASSOCIATE, 'Associate'),
    ]
    MISS = 'MS'
    MADAM = 'MD'
    MISTER = 'MR'
    DOCTOR = 'DR'
    CITIZEN = 'CT'
    TITLE_OPTIONS = [
        (MISS, 'Miss'),
        (MADAM, 'Madam'),
        (MISTER, 'Mister'),
        (DOCTOR, 'Doctor'),
        (CITIZEN, 'Citizen')
    ]

    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    title = models.CharField(
        max_length=2,
        choices=TITLE_OPTIONS,
        default=CITIZEN,
    )
    author_status = models.CharField(
        max_length=2,
        choices=AUTHOR_OPTIONS,
        default=ASSOCIATE,
    )

    def update_rating(self):
        post_rating = self.post_set.all().aggregate(postRating=Sum('rating'))
        comment_rating = self.user.comment_set.all().aggregate(commentRating=Sum('rating'))
        self.rating = post_rating.get('postRating') * 3 \
                      + comment_rating.get('commentRating')
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)

    ARTICLES = 'AR'
    NEWS = 'NW'
    TYPE_OPTIONS = [
        (ARTICLES, 'Article'),
        (NEWS, 'News'),
    ]

    type = models.CharField(
        max_length=2,
        choices=TYPE_OPTIONS,
        default=NEWS,
    )

    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.TextField()
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating != 0:
            self.rating -= 1
            self.save()

    def preview(self):
        if len(self.text) >= 124:
            return self.text[0, 124] + '...'
        else:
            return self.text


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    title = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()

    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating != 0:
            self.rating -= 1
            self.save()
