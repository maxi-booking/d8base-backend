"""
The d8b admin module
"""
from django.contrib import admin
from django_otp.admin import OTPAdminSite

admin.site.__class__ = OTPAdminSite
