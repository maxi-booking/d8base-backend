"""The setup module for the d8base-backend"""
import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()
DESC = 'The REST server for the d8base.com'

setup(
    name='d8base-backend',
    version='0.0.1',
    description=DESC,
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/maxi-booking/d8base-backend',
    author='maxi-booking',
    author_email='info@maxi-booking.com',
    license="GPL-3.0",
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.7.0',
    packages=find_packages(
        exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),
    include_package_data=True,
    install_requires=[
        'Django>=2.0,<3.0',
        'django-environ==0.4.5',
        'django-cors-headers==3.2.1',
        'djangorestframework==3.11.0',
        'drf-extensions==0.6.0',
        'django-extensions==2.2.8',
        'django-debug-toolbar==2.2',
        'django-reversion==3.0.5',
        'django-filter==2.2.0',
        'django-otp==0.8.1',
        'celery==4.4.0',
        'raven==6.10.0',
        'Werkzeug==1.0.0',
        'phonenumbers==8.11.3',
        'qrcode==6.1',
        'redis==3.4.1',
        'psycopg2==2.8.4',
    ],
)
