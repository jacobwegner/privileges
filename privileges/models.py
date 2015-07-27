from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone

from privileges.registration import registry


class Privilege(models.Model):

    label = models.CharField(max_length=75, db_index=True)
    verbose_name = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.verbose_name


class Grant(models.Model):

    grantor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="grants_given")
    grantee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="grants_received")
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(null=True, blank=True)
    privilege = models.ForeignKey(Privilege)
    redelegate_count = models.IntegerField(default=0)
    date_created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return u"%s grants '%s' privilege to %s" % (
            self.grantor, self.privilege, self.grantee
        )


def has_privilege(user, privilege):
    if not hasattr(user, "grants_received"):
        return False

    now = timezone.now()

    return user.grants_received.filter(
        privilege__label__iexact=privilege,
        start__lte=now
    ).filter(
        Q(end__isnull=True) | Q(end__gt=now)
    ).exists()


registry.register(has_privilege)
