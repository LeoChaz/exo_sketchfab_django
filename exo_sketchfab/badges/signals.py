__author__ = 'leomaltrait'

from django.dispatch import Signal


user_signedup = Signal(providing_args=["user"])
model_created = Signal(providing_args=["model", "model3d_owner"])
model_viewed = Signal(providing_args=["model", "model3d_owner"])

