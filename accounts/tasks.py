from datetime import timedelta
from accounts.models import Notification
from card.models import CCCDCard, BHYTCard
from celery import shared_task
from django.utils.timezone import now, make_aware
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings

def create_card_notification(card, title, card_type, days_remaining):
    """Creates a notification for a card."""
    if days_remaining > 0:
        description = f"{title} của bạn sẽ hết hạn sau {days_remaining} ngày!"
    elif days_remaining == 0:
        description = f"{title} của bạn đã hết hạn trong ngày hôm nay! Vui lòng cập nhật."
    else:
        description = f"{title} của bạn đã hết hạn {abs(days_remaining)} ngày, vui lòng cập nhật."

    is_expired = days_remaining <= 0

    return Notification(
        user=card.user,
        title=title,
        description=description,
        is_expired=is_expired,
        type=card_type
    )

def process_card_notifications(card_queryset, card_type, title):
    """Processes notifications for a given card type."""
    current_date = now()
    notifications_to_create = []

    for card in card_queryset:
        try:
            expire_date = datetime.strptime(card.expire_date, "%d/%m/%Y")

            expire_date = make_aware(expire_date)
            days_remaining = (expire_date - current_date).days

            # Check if a similar notification already exists within the last 30 days
            thirty_days_ago = current_date - timedelta(days=30)
            existing_notification = Notification.objects.filter(
                user=card.user,
                title=title,
                created_at__gte=thirty_days_ago
            ).exists()

            if -30 <= days_remaining <= 30 and not existing_notification:
                notification = create_card_notification(card, title, card_type, days_remaining)
                notifications_to_create.append(notification)
                print(f"Scheduled Notification for {title} {card.user.username}: {notification.description}")

        except ValueError as e:
            print(f"Invalid expire date format: {card.expire_date} for {card.user.username}. Error: {e}")
        except AttributeError as e:
            print(f"Card {card.pk} has no expire_date. Error: {e}")

    if notifications_to_create:
        Notification.objects.bulk_create(notifications_to_create)
        print(f"Created {len(notifications_to_create)} notifications for {title}.")


@shared_task(bind=True)
def schedule_notification(self):
    """Schedules notifications for CCCD and BHYT cards."""
    notification_configs = [
        {"queryset": CCCDCard.objects.all(), "card_type": "cccd", "title": "Căn cước công dân"},
        {"queryset": BHYTCard.objects.all(), "card_type": "bhyt", "title": "Bảo hiểm y tế"},
    ]

    for config in notification_configs:
        process_card_notifications(config["queryset"], config["card_type"], config["title"])

    print("All scheduled tasks completed successfully!")

@shared_task(bind=True, retry_backoff=True, retry_kwargs={'max_retries': 3})  # Added retry mechanism
def send_expired_notification_emails(self):
    """
    Sends email notifications for expired cards (is_expired=True).
    """
    expired_notifications = Notification.objects.filter(is_expired=True)

    for notification in expired_notifications:
        try:
            subject = f"Thông báo: {notification.title} của bạn đã hết hạn!"
            message = f"""
                Chào {notification.user.fullname},

                Thông báo này nhằm thông báo cho bạn rằng {notification.title} của bạn đã hết hạn. 
                Vui lòng cập nhật {notification.title} của bạn trong thời gian sớm nhất.

                Trân trọng,
                VNEiD
            """

            send_mail(subject, message, settings.EMAIL_HOST_USER, [notification.user.email])
            print(f"Sent email notification for expired {notification.title} to {notification.user.username}")

        except Exception as exc:
            print(f"Error sending email notification for expired {notification.title} to {notification.user.username}: {exc}")
            self.retry(exc=exc)  # Retry the task on exception

    print("Finished checking and sending expired notification emails.")