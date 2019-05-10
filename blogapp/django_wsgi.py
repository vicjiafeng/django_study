#!/usr/bin/env python
# coding:utf-8
import os
import sys

reload(sys)
sys.setdefaultcoding('utf8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogapp.settings")
from django.core.wsgi import get_wsgi_application
applicetion = get_wsgi_application()
