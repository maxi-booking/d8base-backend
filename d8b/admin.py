"""The d8b admin module."""
from django.conf import settings
from django.contrib import admin
from django_otp.admin import OTPAdminSite

if not settings.TESTS:
    admin.site.__class__ = OTPAdminSite
