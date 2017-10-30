#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
from core import choices

class CMUser(AbstractUser):
    phone = models.CharField(verbose_name = u'Phone number', max_length = 14, blank = True, null = True)



