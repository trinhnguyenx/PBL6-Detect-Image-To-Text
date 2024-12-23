from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .serializer import CCCDCardSerializer, GPLXCardSerializer, BHYTCardSerializer
from .models import CCCDCard, GPLXCard, BHYTCard
from accounts.models import CustomUser
# Create your views here.

class CCCDViewSet(viewsets.ModelViewSet):
    queryset = CCCDCard.objects.all()
    serializer_class = CCCDCardSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = CCCDCard.objects.filter(user_id=user_id)
            if not queryset.exists():
                raise NotFound(detail="Không tìm thấy thẻ CCCD cho user_id này.")
        else:
            queryset = CCCDCard.objects.all()

        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        self.perform_destroy(instance)
        user.is_verified = False
        user.save()
        affected_users = CustomUser.objects.filter(cccd_cards__isnull=True)
        affected_users.update(is_verified=False)
        return Response(
            {"message": "Thẻ CCCD đã được xóa và trạng thái xác minh của người dùng đã cập nhật."},
            status=status.HTTP_204_NO_CONTENT,
        )
class GPLXViewSet(viewsets.ModelViewSet):
    queryset = GPLXCard.objects.all()
    serializer_class = GPLXCardSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)

        if user_id:
            queryset = GPLXCard.objects.filter(user_id=user_id)
            if not queryset.exists():
                raise NotFound(detail="Không tìm thấy thẻ GPLX cho id này.")
        else:
            queryset = GPLXCard.objects.all()

        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        self.perform_destroy(instance)
        user.is_gplx = False
        user.save()
        affected_users = CustomUser.objects.filter(gplx_cards__isnull=True)
        affected_users.update(is_gplx=False)
        return Response(
            {"message": "Thẻ GPLX đã được xóa và trạng thái xác minh GPLX của người dùng đã cập nhật."},
            status=status.HTTP_204_NO_CONTENT,
        )

class BHYTViewSet(viewsets.ModelViewSet):
    queryset = BHYTCard.objects.all()
    serializer_class = BHYTCardSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)

        if user_id:
            queryset = BHYTCard.objects.filter(user_id=user_id)
            if not queryset.exists():
                raise NotFound(detail="Không tìm thấy thẻ BHYT cho id này.")
        else:
            queryset = BHYTCard.objects.all()
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        self.perform_destroy(instance)

        user.is_bhyt = False
        user.save()
        affected_users = CustomUser.objects.filter(bhyt_cards__isnull=True)
        affected_users.update(is_bhyt=False)
        return Response(
            {"message": "Thẻ BHYT đã được xóa và trạng thái xác minh BHYT của người dùng đã cập nhật."},
            status=status.HTTP_204_NO_CONTENT,
        )