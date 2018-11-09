from django import forms


class FirstTaskForm(forms.Form):
    number = forms.IntegerField(required=False)