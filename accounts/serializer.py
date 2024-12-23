from rest_framework import serializers
from .models import CustomUser, Notification


class CustomUserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(required=False)  # Make 'age' optional

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'fullname', 'password', 'age', 'role', 'avatar','username','is_verified','is_bhyt', 'is_gplx']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        age = validated_data.get('age', 18)
        role = validated_data.get('role', 'user')
        avatar = validated_data.get('avatar', 'https://www.gravatar.com/avatar/?d=mp')
        is_verified = validated_data.get('is_verified', False)
        is_bhyt = validated_data.get('is_bhyt', False)
        is_gplx = validated_data.get('is_gplx', False)
        fullname = validated_data.get('fullname', '')

        user = CustomUser.objects._create_user(
            email=validated_data['email'],
            fullname=fullname,
            password=validated_data['password'],
            age=age,
            role=role,
            avatar=avatar,
            username=validated_data['username'],
            is_verified=is_verified,
            is_bhyt=is_bhyt,
            is_gplx=is_gplx,
        )
        user.save()
        return user


class SendMailSerializer(serializers.Serializer):
    address = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


