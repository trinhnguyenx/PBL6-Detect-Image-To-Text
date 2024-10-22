from rest_framework import serializers

from .models import CustomUser
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name','password']
        # or fileds = '_all_'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects._create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        user.save()
        return user

class SendMailSerializer(serializers.Serializer):
    address = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()


