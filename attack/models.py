from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField, IntegerField
from django.db.models.fields.related import OneToOneField
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import widgets
from django.forms.widgets import TextInput
import sys

class Account(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    balance = IntegerField("Balance", default=5000, validators=[MinValueValidator(0)])
    name = CharField(max_length=20, null=True, blank=True)

class Foo(models.Model):
    name = CharField(max_length=20, null=True, blank=True)

class WithdrewForm(forms.Form):
    current_balance = forms.IntegerField(validators=[MinValueValidator(0)], widget=forms.TextInput(attrs={'readonly':True}))
    withdrew = forms.IntegerField(validators=[MinValueValidator(0)])

    def clean_withdrew(self):
        withdraw = self.cleaned_data['withdrew']
        current_balance = self.cleaned_data['current_balance']
        print(f"{withdraw}, {current_balance}", file=sys.stderr)
        if withdraw > current_balance:
            raise ValidationError(f"Can't withraw more than what your have ({current_balance}).")

        return withdraw 

