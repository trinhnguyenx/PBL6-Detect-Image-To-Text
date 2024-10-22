
from django.http import BadHeaderError
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.core.mail import send_mail
from django.conf import settings

from .models import CustomUser
from .serializer import CustomUserSerializer, SendMailSerializer


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
        username = request.data['username']
        password = request.data['password']

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
                user = authenticate(request, username=user.username, password=password)
            except ObjectDoesNotExist:
                return Response({'message': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = authenticate(request, username=username, password=password)
        if user:
            refresh_token = RefreshToken.for_user(user)
            access_token = AccessToken.for_user(user)
            return Response({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'password': user.password,
                'accessToken': str(access_token),
                'refreshToken': str(refresh_token)
            }, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

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


