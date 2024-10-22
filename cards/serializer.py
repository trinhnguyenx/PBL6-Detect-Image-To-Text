#! /usr/bin/python
# Copyright (C) 2024 Paradox
# Release: v2.4.4
# @link olivia.paradox.ai


__author__ = "trinh.nguyen@paradox.ai"
__date__ = "22/10/2024 15:06"

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import CCCDCard

class CCCDCardSerializer(serializers.ModelSerializer):
    number = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(queryset=CCCDCard.objects.all())]
    )
    class Meta:
        model = CCCDCard
        fields = ['uuid','fullname', 'number', 'dateOfBirth', 'sex', 'placeOfOrigin', 'placeOfResidence', 'dateOfExpiry', 'user']
