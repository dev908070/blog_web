from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User


def send_blog_update_email(user_email, blog_title, blog_url):
    subject = f'New Blog Post: {blog_title}'
    html_message = render_to_string('emails/blog_update.html', {'blog_title': blog_title, 'blog_url': blog_url})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, plain_message, from_email, [user_email], html_message=html_message)

def notify_all_users_about_blog(blog_title, blog_url):
    users = User.objects.all()
    for user in users:
        send_blog_update_email(user.email, blog_title, blog_url)
