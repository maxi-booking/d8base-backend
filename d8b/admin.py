"""The d8b admin module."""
import adminactions.actions as actions
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import site
from django_otp.admin import OTPAdminSite

if not settings.TESTS:
    admin.site.__class__ = OTPAdminSite

actions.add_to_site(site)
