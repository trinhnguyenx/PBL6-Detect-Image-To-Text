
from django.http import BadHeaderError, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, Notification
from .serializer import CustomUserSerializer, SendMailSerializer, NotificationSerializer
from django.contrib.auth.hashers import check_password
from card.models import CCCDCard
from io import BytesIO
import qrcode
from rest_framework.response import Response
from rest_framework import viewsets
# Create your views here.

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(password, user.password):
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

        refresh_token = RefreshToken.for_user(user)
        access_token = AccessToken.for_user(user)

        return Response({
            'id': user.id,
            'fullname': user.fullname,
            'username': user.username,
            'role': user.role,
            'email': user.email,
            'age': user.age,
            'avatar': user.avatar,
            'is_verified': user.is_verified,
            'is_bhyt': user.is_bhyt,
            'is_gplx': user.is_gplx,
            'password': user.password,
            'accessToken': str(access_token),
            'refreshToken': str(refresh_token)
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    if request.method == 'POST':
        try:
            token = Token.objects.get(user=request.user)
            token.delete()

            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE','PUT'])
def delete_update_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User Deleted Successfully"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        try:
            user = CustomUser.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response({"error": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_user(request):
    try:
        users = CustomUser.objects.all()
    except ObjectDoesNotExist:
        return Response({"error": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    user = request.user
    serializer = CustomUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_mail_page(request):
    serializer = SendMailSerializer(data=request.data)
    if serializer.is_valid():
        address = serializer.validated_data['address']
        subject = serializer.validated_data['subject']
        message = serializer.validated_data['message']

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
            return Response(
                {"result": "Email sent successfully"},
                status=status.HTTP_200_OK
            )
        except BadHeaderError:
            return Response(
                {"error": "Invalid header found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Error sending email: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_qr_code(cccd_card):
    """
    Hàm tạo QR code từ dữ liệu thẻ CCCD và trả về QR code dưới dạng nhị phân (image/png).
    """
    # Tạo dữ liệu để mã hóa vào QR code
    data_to_encode = (
        f"Số CCCD: {cccd_card.id}, Họ tên: {cccd_card.name}, "
        f"Ngày Sinh: {cccd_card.dob}, Quốc tịch: {cccd_card.nationality}, "
        f"Giới tính: {cccd_card.gender}, Ngày cấp: {cccd_card.issue_date}, "
        f"Nơi cấp: {cccd_card.origin_place}, Ngày hết hạn: {cccd_card.expire_date}"
    )

    # Tạo QR code từ dữ liệu
    qr = qrcode.make(data_to_encode)

    # Lưu QR code vào bộ nhớ đệm
    buffer = BytesIO()
    qr.save(buffer, 'PNG')
    buffer.seek(0)

    # Trả về QR code dưới dạng nhị phân (Blob) trong response
    return HttpResponse(buffer, content_type='image/png')

@api_view(['GET'])
def get_cccd_qrcode(request):
    """
    API để lấy thông tin thẻ CCCD và tạo QR code cho user_id cụ thể.
    """
    id_qrcode = request.query_params.get('id_qrcode', None)
    if not id_qrcode:
        return Response({"detail": "user_id không được cung cấp."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Tìm thẻ CCCD theo user_id
        cccd_card = CCCDCard.objects.get(user_id=id_qrcode)
    except CCCDCard.DoesNotExist:
        return Response({"detail": "Không tìm thấy thẻ CCCD cho user_id này."}, status=status.HTTP_404_NOT_FOUND)

    # Gọi hàm để tạo QR code và trả về hình ảnh QR code
    return generate_qr_code(cccd_card)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)

        if user_id:
            queryset = Notification.objects.filter(user_id=user_id)
            if not queryset.exists():
                raise NotFound(detail="Không tìm thấy thông tin cho id này.")
        else:
            queryset = Notification.objects.all()

        sort_order = self.request.query_params.get('order', 'asc').lower()

        if sort_order == 'asc':
            queryset = queryset.order_by('-created_at')
        elif sort_order == 'desc':
            queryset = queryset.order_by('created_at')
        else:
            raise ValueError("Giá trị của 'order' phải là 'asc' hoặc 'desc'.")

        return queryset
