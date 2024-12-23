from django.urls import path, include
from .views import register_user, logout_user, login_user, get_user, delete_update_user, get_me, send_mail_page,get_cccd_qrcode, NotificationViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'notification', NotificationViewSet)
urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('users/', get_user, name='getUser'),
    path('users/<int:user_id>/', delete_update_user, name="deleteUpdateUser"),
    path('me/', get_me, name='getMe'),
    path('sendmail/', send_mail_page, name='send_mail'),
    path('qrcode/', get_cccd_qrcode, name='getQrCode'),
    path('', include(router.urls)),
]