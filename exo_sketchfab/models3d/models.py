__author__ = 'leomaltrait'

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class Model3d(models.Model):
    """ Model to represent 3D models """
    model3d_owner = models.ForeignKey(AUTH_USER_MODEL, related_name='model3d_owner', verbose_name=_('model3d_owner'))

    date_added = models.DateTimeField(_('date published'),
                                      default=now)

    name = models.CharField(_('name'), max_length=140, unique=False)

    description = models.TextField(_('description'),
                                   blank=True)

    view_count = models.PositiveIntegerField(_('view count'),
                                             default=0,
                                             editable=False)

    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'
        verbose_name = _('Model3d')
        verbose_name_plural = _('Models3d')

    def __str__(self):
        return self.name






