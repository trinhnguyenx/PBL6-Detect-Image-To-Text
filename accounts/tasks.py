from django.utils.timezone import now, make_aware
from datetime import datetime
from accounts.models import Notification
from card.models import CCCDCard, BHYTCard
from celery import shared_task
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def process_card_notifications(card_queryset, card_type, title):
    """
    Xử lý thông báo cho các loại thẻ (CCCD, GPLX, BHYT).
    """
    current_date = now()
    notifications_to_create = []

    for card in card_queryset:
        try:
            expire_date = datetime.strptime(card.expire_date, "%d/%m/%Y")
            expire_date = make_aware(expire_date)
            days_remaining = (expire_date - current_date).days

            # Kiểm tra thông báo đã tồn tại
            notification_today = Notification.objects.filter(
                user=card.user,
                title=title,
                description__icontains="hết hạn trong ngày hôm nay"
            ).exists()

            existing_notification = Notification.objects.filter(
                user=card.user,
                title=title,
                description__icontains=f"{abs(days_remaining)} ngày"
            ).exists()
            expried_filter = -30 <= days_remaining <= 30
            if  expried_filter and not existing_notification and not notification_today:
                if days_remaining > 0:
                    description = f"{title} của bạn sẽ hết hạn sau {days_remaining} ngày!"
                elif days_remaining == 0:
                    description = f"{title} của bạn đã hết hạn trong ngày hôm nay! Vui lòng cập nhật."
                else:
                    description = f"{title} của bạn đã hết hạn {abs(days_remaining)} ngày, vui lòng cập nhật."

                is_expired = days_remaining <= 0

                notification = Notification(
                    user=card.user,
                    title=title,
                    description=description,
                    is_expired=is_expired,
                    type=card_type
                )
                notifications_to_create.append(notification)
                print(f"Scheduled Notification for {title} {card.user.username}: {description}")

        except ValueError as e:
            print(f"Ngày hết hạn không đúng định dạng: {card.expire_date}. Lỗi: {e}")

    if notifications_to_create:
        Notification.objects.bulk_create(notifications_to_create)
        print(f"Created {len(notifications_to_create)} notifications for {title}.")

@shared_task(bind=True)
def schedule_notification(self):
    """
    Task tự động tạo thông báo cho các loại thẻ: CCCD, GPLX, BHYT.
    """
    notification_configs = [
        {
            "queryset": CCCDCard.objects.all(),
            "card_type": "cccd",
            "title": "Căn cước công dân"
        },
        {
            "queryset": BHYTCard.objects.all(),
            "card_type": "bhyt",
            "title": "Bảo hiểm y tế"
        }
    ]

    for config in notification_configs:
        process_card_notifications(
            config["queryset"],
            config["card_type"],
            config["title"]
        )

    print("All scheduled tasks completed successfully!")
