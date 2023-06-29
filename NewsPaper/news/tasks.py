from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from NewsPaper import settings
from news.models import Post, Category


@shared_task
def new_post_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__category=instance.category
    ).values_list('email', flat=True)

    subject = f'New post was added in {instance.category} category'

    text_content = (
        f'Title: {instance.title}\n'
        f'Prevew: {instance.preview}\n\n'
        f'Post link: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'We have a new content for you: <br> {instance.title}<br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Hurry up to read!</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

@shared_task
def weekly_notification():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'weekly_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Посты за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()