from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)
    def __str__(self):
        return self.authorUser.username

    def update_rating(self):
        """ Фунция обновления рэйтинга. функ.Sum суммирует все знаяения поля 'rating' """

        postRate = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRate.get('postRating')

        commentRate = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRate.get('commentRating')
        self.ratingAuthor = pRat * 3 + cRat
        self.save()
#функции cRat/pRat являются промежуточным, они необходимы для получения данных от функции postRate/commentRate


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')
    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.author


    NEWS = 'NW'
    ARTICAL = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICAL, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICAL)
    dateCreations = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=id(1), related_name='ForPostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.title} \n {self.text[0:123]} + {...}'

    def get_absolute_url(self):
        return "/news/%i/" % self.id
    def __str__(self):
        return self.title


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.postThrough


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreations = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
