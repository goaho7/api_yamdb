from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers


class UsernameCharField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 150)
        self.validators.append(UnicodeUsernameValidator())
        super().__init__(**kwargs)
