from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from misago.forms import Form
import misago.captcha
from misago.timezones import tzlist
from misago.users.models import User
from misago.users.validators import validate_password, validate_email


class UserRegisterForm(Form):
    username = forms.CharField(max_length=15)
    email = forms.EmailField(max_length=255)
    email_rep = forms.EmailField(max_length=255)
    password = forms.CharField(max_length=255,widget=forms.PasswordInput)
    password_rep = forms.CharField(max_length=255,widget=forms.PasswordInput)
    captcha_qa = captcha.QACaptchaField()
    recaptcha = captcha.ReCaptchaField()
    accept_tos = forms.BooleanField(required=True,error_messages={'required': _("Acceptation of board ToS is mandatory for membership.")})
    
    validate_repeats = (('email', 'email_rep'), ('password', 'password_rep'))
    repeats_errors = [{
                       'different': _("Entered addresses do not match."), 
                       },
                      {
                       'different': _("Entered passwords do not match."),
                       }]
    
    layout = [
              (
               None,
               [('username', {'label': _('Username'), 'help_text': _("Your displayed username. Between 3 and 15 characters, only letters and digits are allowed."),'attrs': {'placeholder': _("Enter your desired username")}})]
               ),
              (
               None,
               [('nested', [('email', {'label': _('E-mail address'), 'help_text': _("Working e-mail inbox is required to maintain control over your forum account."), 'attrs': {'placeholder': _("Enter your e-mail")}, 'width': 50}), ('email_rep', {'attrs': {'placeholder': _("Repeat your e-mail")}, 'width': 50})]), 
               ('nested', [('password', {'label': _('Password'), 'help_text': _("Password you will be using to sign in to your account. Make sure it's strong."), 'has_value': False, 'attrs': {'placeholder': _("Enter your password")}, 'width': 50}), ('password_rep', {'has_value': False, 'attrs': {'placeholder': _("Repeat your password")}, 'width': 50})])]
               ),
              (
               None,
               ['captcha_qa', 'recaptcha']
               ),
              (
               None,
               [('accept_tos', {'label': _("Forum Terms of Service"), 'inline': _("I have read and accept this forums Terms of Service.")})]
               ),
              ]
        
    def clean_username(self):
        new_user = User.objects.get_blank_user()
        new_user.set_username(self.cleaned_data['username'])
        try:
            new_user.full_clean()
        except ValidationError as e:
            new_user.is_username_valid(e)
        return self.cleaned_data['username']
        
    def clean_email(self):
        new_user = User.objects.get_blank_user()
        new_user.set_email(self.cleaned_data['email'])
        try:
            new_user.full_clean()
        except ValidationError as e:
            new_user.is_email_valid(e)
        return self.cleaned_data['email']
        
    def clean_password(self):
        new_user = User.objects.get_blank_user()
        new_user.set_password(self.cleaned_data['password'])
        try:
            new_user.full_clean()
        except ValidationError as e:
            new_user.is_password_valid(e)
        validate_password(self.cleaned_data['password'])
        return self.cleaned_data['password']