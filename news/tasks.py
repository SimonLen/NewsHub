from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from celery import shared_task
from datetime import datetime, timedelta
from .models import Post, Category
from NewsHub import settings


@shared_task
def new_post_in_category_notifier():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(creation_date__gte=last_week)
    categories = set(posts.values_list('category__theme', flat=True))
    subscribers = set(Category.objects.filter(theme__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_new_post_notification(preview, pk, title, subs):
    html_content = render_to_string(
        'post_created_email_celery.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subs,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

