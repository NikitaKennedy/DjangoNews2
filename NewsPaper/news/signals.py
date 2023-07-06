from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import *

@receiver(post_save, sender=Post)
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
