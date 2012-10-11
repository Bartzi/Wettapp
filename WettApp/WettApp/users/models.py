# -*- coding: utf-8 -*-

import random
import string

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Model for any aditional data we need for the User model."""
    user = models.OneToOneField(User)   # this is required
    activation_key = models.CharField(max_length=30, editable=False)
    buddy_profiles = models.ManyToManyField('self', blank=True)

    def __unicode__(self):
        return 'Profile of {0}'.format(self.user.username)

    def save(self, *args, **kwargs):
        self.activation_key = self.__create_key()
        super(UserProfile, self).save(*args, **kwargs)

    def __create_key(self):
        return ''.join(random.choice(string.ascii_letters + string.digits)
                        for n in xrange(30))

    def buddies(self):
        return User.objects.filter(userprofile__in=self.buddy_profiles.all())
