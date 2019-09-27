#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class LoginAuthenticationForm(AuthenticationForm):
    """Form for authenticating a requested user.
    Authenticates a user against the provided username
    and password.

    User can use as username his email or his actual username.
    """
    username = forms.CharField(
        required=True, max_length=50, widget=TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control',
            'required': 'true'}))

    password = forms.CharField(required=True, widget=PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'required': 'true'}))

    remember_me = forms.BooleanField(
        required=False, widget=forms.CheckboxInput())

    def clean_remember_me(self):
        # if not self.cleaned_data.get('remember_me'):
        #     self.request.session.set_expiry(0)
        # checked or not keep loged in
        self.request.session.set_expiry(0)
