__author__ = 'leomaltrait'

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

import datetime
import pytz

from .signals import user_signedup, model_created, model_viewed

from ..models3d.models import Model3d

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class Badges(models.Model):
    """ Model to represent Badges """

    name = models.CharField(max_length=140)

    class Meta:
        verbose_name = u'Badges Model'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class BadgesExtended(models.Model):

    badge = models.OneToOneField(Badges, related_name='badgesextended')

    # Many users can have many badges
    badge_owners = models.ManyToManyField(User, related_name='badge_owner',
                                   verbose_name=_('badge_owner'),
                                   blank=True)

    date_obtained = models.DateTimeField(_('date obtained'),
                                      default=now)




def add_badge(user, name):

    # Get badge if already exist, else create it
    try:
        badge = Badges.objects.get(name=name)
        badge_extended = BadgesExtended.objects.get(badge=badge)
    except Badges.DoesNotExist:
        badge = Badges.objects.create(name=name)
        badge_extended = BadgesExtended.objects.create(badge=badge)

    # Check if user already has the badge. If not, give it to her.
    if BadgesExtended.objects.filter(pk=badge_extended.pk, badge_owners=user):
        print("User already has the {} badge!".format(name))
    else:
        badge_extended.badge_owners.add(user)
        print("User just received {} badge!".format(name))


# Checked when access to current user infos in users/views.py
def check_user_inscription_date(sender, **kwargs):

    today = datetime.datetime.now()
    one_year = today - datetime.timedelta(days=365)

    user_inscription_date = kwargs['user'].date_joined

    is_long_enough = (user_inscription_date  <= pytz.utc.localize(one_year))

    if is_long_enough:
        add_badge(user=kwargs['user'], name='Pionneer')


user_signedup.connect(check_user_inscription_date)


# Checked when create new model in models3d/serializers.py
def check_user_uploaded_model(sender, **kwargs):

    model3d_owner = kwargs["model3d_owner"]
    count_model = Model3d.objects.filter(model3d_owner=model3d_owner).count()

    if count_model == 5 :
        add_badge(model3d_owner, name='Collector')

    # Could delete this elif
    elif count_model > 5:
        print("User just uploaded a model. User already has a Collector Badge!")

    else:
        print("User just uploaded a model. No new badge yet.")


model_created.connect(check_user_uploaded_model)


# Checked if user has more than 1000 views for a model in models3d/views.py
def check_user_model_viewed(sender, **kwargs):

    model3d_owner = kwargs["model3d_owner"]
    model = kwargs['model']
    count = model.view_count

    # Could delete ">"
    if count >= 1000:
        add_badge(model3d_owner, name='Star')

model_viewed.connect(check_user_model_viewed)
