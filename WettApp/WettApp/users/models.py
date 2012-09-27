# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.db import models
from django.dispatch import receiver


class UserProfile(models.Model):
    """Model for any aditional data we need for the User model."""
    user = models.OneToOneField(User)   # this is required
    buddies = models.ManyToManyField(User, blank=True, related_name='buddies')

    def __unicode__(self):
        return 'Profile of {0}'.format(self.user.username)


@receiver(m2m_changed, sender=UserProfile.buddies.through)
def update_buddies(sender, **kwargs):
    """
    Signal receiver for buddy changes.

    Each time a User's buddies are changed, this function updates the
    m2m relationship, so for every relationship tuple there is a reverse
    one. This makes sure that when person A is a buddy of person B, B is also
    a buddy of A.
    Unfortunately, the m2m_changed signal is buggy (#6707), so we have no
    possibility to know what exactly has changed. Therefore, we update all
    relationships with every change.
    """
    if kwargs['action'] == 'post_add':
        user = kwargs['instance'].user
        # update added relationships
        for buddy in kwargs['instance'].buddies.all():
            buddy_profile = buddy.get_profile()
            if not buddy_profile.buddies.filter(pk=user.pk).exists():
                buddy_profile.buddies.add(user)
        # update removed relationships
        for buddy_profile in UserProfile.objects.filter(buddies__pk=user.pk):
            buddy = buddy_profile.user
            user_profile = user.get_profile()
            if not user_profile.buddies.filter(pk=buddy.pk).exists():
                buddy_profile.buddies.remove(user)
