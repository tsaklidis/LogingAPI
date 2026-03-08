import datetime
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models

from home_logs.utils.unique import get


@python_2_unicode_compatible
class Token(models.Model):

    key = models.CharField(max_length=50, unique=True)

    user = models.ForeignKey(
        get_user_model(), related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )

    name = models.CharField(max_length=64)

    created_on = models.DateTimeField(auto_now_add=True, null=True)

    expiration = models.DateTimeField(auto_now_add=False, null=True)

    invalid = models.BooleanField(default=False)

    @property
    def expired(self):
        if not self.expiration:
            return False
        else:
            if self.expiration < timezone.now():
                return True
            return False

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = get(40)
        super(Token, self).save(*args, **kwargs)

    class Meta:
        # ensure user and name are unique
        unique_together = (('user', 'name'),)
        indexes = [
            models.Index(fields=['user', 'invalid', 'expiration']),
        ]

    def __str__(self):
        return 'Token of:{}'.format(self.user)
