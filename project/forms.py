from django import forms
import json
from django.core.exceptions import ValidationError


class IntegersList(forms.CharField):
    def __init__(self, required=False, **kwargs):
        kwargs['required'] = required
        super().__init__(**kwargs)

    def clean(self, value):
        value = super().clean(value)

        if value is None or value == '':
            if self.required:
                raise ValidationError('required IntegerListType')
            return []

        try:
            value = json.loads(value)
        except:
            raise ValidationError('invalid IntegerListType')

        if not isinstance(value, list):
            raise ValidationError('invalid IntegerListType')

        if self.required and len(value) <= 0:
            raise ValidationError('IntegerListType cannot be empty')

        for x in value:
            if not isinstance(x, int):
                raise ValidationError('invalid IntegerListType')

        return value


class SecondTaskForm(forms.Form):
    l = IntegersList(required=True)
    p = forms.IntegerField()
