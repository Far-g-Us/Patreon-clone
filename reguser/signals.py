from django.db.models.signals import post_save
from django.dispatch import receiver
from home.models import Subscription
from django.core.mail import send_mail

@receiver(post_save, sender=Subscription)
def send_subscription_notification(sender, instance, created, **kwargs):
    if created:
        subject = f'New Subscription: {instance.user.username}'
        message = f'User {instance.user.username} subscribed to your tier "{instance.tier.name}"!'
        send_mail(
            subject,
            message,
            'noreply@yourpatreonclone.com',
            [instance.tier.creator.email],
            fail_silently=False,
        )