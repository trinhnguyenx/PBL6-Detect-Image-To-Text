#! /usr/bin/python
# Copyright (C) 2024 Paradox
# Release: v2.4.4
# @link olivia.paradox.ai


__author__ = "trinh.nguyen@paradox.ai"
__date__ = "22/10/2024 15:06"

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import CCCDCard, BHYTCard, GPLXCard

class CCCDCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = CCCDCard
        fields = ['uuid','dob','nationality','id', 'name', 'gender', 'expire_date', 'type', 'origin_place', 'current_place','issue_date','user','personal_identifi','is_valid','images','images_behind']

class BHYTCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = BHYTCard
        fields = ['uuid','name', 'id', 'dob', 'gender','iplace', 'expire_date','ihos','type', 'user','issue_date','is_valid','images']

class GPLXCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPLXCard
        fields = ['uuid','name', 'dob', 'id', 'iplace', 'origin_place', 'issue_date','expire_date','nationality','level','type', 'user','is_valid','images']