#! /usr/bin/python
# Copyright (C) 2024 Paradox
# Release: v2.4.4
# @link olivia.paradox.ai


__author__ = "trinh.nguyen@paradox.ai"
__date__ = "22/10/2024 15:14"

from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import CCCDViewSet, BHYTViewSet, GPLXViewSet

router = DefaultRouter()
router.register(r'cccd', CCCDViewSet)
router.register(r'bhyt', BHYTViewSet)
router.register(r'gplx', GPLXViewSet)


urlpatterns = [
    path('', include(router.urls)),
]