# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Model for any aditional data we need for the User model."""
    user = models.OneToOneField(User)   # this is required
    buddies = models.ManyToManyField(User, blank=True, related_name='buddies')

    def __unicode__(self):
        return 'Profile of {0}'.format(self.user.username)
