__author__ = 'leomaltrait'

from django.db import IntegrityError


class AlreadyExistsError(IntegrityError):
    pass
