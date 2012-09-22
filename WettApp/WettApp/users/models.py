# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Model for any aditional data we need for the User model."""
    user = models.OneToOneField(User)   # this is required

    buddies = models.ManyToManyField(User, related_name='buddies')
