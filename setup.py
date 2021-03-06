"""The setup module for the d8base-backend."""
import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()
DESC = "The REST server for the d8base.com"

setup(
    name="d8base-backend",
    version="0.0.1",
    description=DESC,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/maxi-booking/d8base-backend",
    author="maxi-booking",
    author_email="info@maxi-booking.com",
    license="GPL-3.0",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8.0",
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    install_requires=[
        "Django>=3.0.7,<3.1",
        "django-environ==0.4.5",
        "django-cors-headers==3.5.0",
        "django-modeltranslation==0.15.2",
        "django-admin-sortable==2.2.3",
        "djangorestframework==3.11.0",
        "drf-extensions==0.6.0",
        "djangorestframework-gis==0.16",
        "django-rest-registration==0.5.6",
        "django-extra-fields==3.0.2",
        "django-clearcache==1.1.1",
        "django-extensions==3.0.9",
        "django-debug-toolbar==3.1.1",
        "django-reversion==3.0.8",
        "django-filter==2.4.0",
        "django-money==1.1",
        "django-otp==1.0.0",
        "django-adminactions==1.8.1",
        "django-phonenumber-field==5.0.0",
        "django-cities @ git+https://github.com/webmalc/django-cities",
        "django-crispy-forms==1.9.2",
        "django-oauth-toolkit==1.3.2",
        "django-admin-autocomplete-filter==0.6.1",
        "django-imagekit==4.0.2",
        "django-push-notifications==2.0.0",
        "django-elasticsearch-dsl==7.1.4",
        "drf-yasg==1.17.1",
        "celery==4.4.6",
        "Werkzeug==1.0.1",
        "phonenumbers==8.12.10",
        "qrcode==6.1",
        "sentry-sdk==0.18.0",
        "arrow==0.16",
        "redis==3.5.3",
        "psycopg2==2.8.6",
        "python-memcached==1.59",
        "Pillow==7.2.0",
        "pytz==2020.1",
        "translate==3.5.0",
    ],
)
