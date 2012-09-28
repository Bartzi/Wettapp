# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
# from django.db.models.signals import m2m_changed
from django.db import models
# from django.dispatch import receiver


class UserProfile(models.Model):
    """Model for any aditional data we need for the User model."""
    user = models.OneToOneField(User)   # this is required
    buddy_profiles = models.ManyToManyField('self', blank=True)

    def __unicode__(self):
        return 'Profile of {0}'.format(self.user.username)

    def buddies(self):
        return User.objects.filter(userprofile__in=self.buddy_profiles.all())
