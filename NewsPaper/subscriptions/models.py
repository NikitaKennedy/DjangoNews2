from django.db import models
from django.contrib.auth.models import User
from news.models import Category
# Create your models here.

class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to= Category,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
