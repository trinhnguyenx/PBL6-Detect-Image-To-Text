from django.utils.timezone import now, make_aware
from datetime import datetime
from accounts.models import Notification
from card.models import CCCDCard, GPLXCard, BHYTCard
from celery import shared_task
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def process_card_notifications(card_queryset, card_type, title, description_template):
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

            if days_remaining <= 30 and not existing_notification and not notification_today:
                description = description_template.format(days_remaining=days_remaining, days_abs=abs(days_remaining))
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
def schedule_notifications(self):
    """
    Task tự động tạo thông báo cho các loại thẻ: CCCD, GPLX, BHYT.
    """
    notification_configs = [
        {
            "queryset": CCCDCard.objects.all(),
            "card_type": "cccd",
            "title": "Căn cước công dân",
            "description_template": (
                "Căn cước công dân của bạn sẽ hết hạn sau {days_remaining} ngày!"
                if "{days_remaining}" > "0" else
                "Căn cước công dân của bạn đã hết hạn {days_abs} ngày, vui lòng cập nhật."
                if "{days_remaining}" < "0" else
                "Căn cước công dân của bạn đã hết hạn trong ngày hôm nay! Vui lòng cập nhật."
            )
        },
        {
            "queryset": GPLXCard.objects.all(),
            "card_type": "gplx",
            "title": "Giấy phép lái xe",
            "description_template": (
                "Giấy phép lái xe của bạn sẽ hết hạn sau {days_remaining} ngày!"
                if "{days_remaining}" > "0" else
                "Giấy phép lái xe của bạn đã hết hạn {days_abs} ngày, vui lòng cập nhật."
                if "{days_remaining}" < "0" else
                "Giấy phép lái xe của bạn đã hết hạn trong ngày hôm nay! Vui lòng cập nhật."
            )
        },
        {
            "queryset": BHYTCard.objects.all(),
            "card_type": "bhyt",
            "title": "Bảo hiểm y tế",
            "description_template": (
                "Bảo hiểm y tế của bạn sẽ hết hạn sau {days_remaining} ngày!"
                if "{days_remaining}" > "0" else
                "Bảo hiểm y tế của bạn đã hết hạn {days_abs} ngày, vui lòng cập nhật."
                if "{days_remaining}" < "0" else
                "Bảo hiểm y tế của bạn đã hết hạn trong ngày hôm nay! Vui lòng cập nhật."
            )
        }
    ]

    for config in notification_configs:
        process_card_notifications(
            config["queryset"],
            config["card_type"],
            config["title"],
            config["description_template"]
        )

    print("All scheduled tasks completed successfully!")
