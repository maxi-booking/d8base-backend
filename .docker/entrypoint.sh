#!/bin/bash
ip -4 route list match 0/0 | awk '{print $3" hostmaster"}' >> /etc/hosts \
    && exec python3 manage.py runserver 0.0.0.0:8000

