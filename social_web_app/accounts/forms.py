
from django import forms
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import User

# User = get_user_model()


class RegisterForm(forms.ModelForm):
  name = forms.CharField(
    label='Name',
    widget=forms.TextInput(
      attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Enter Name',
        'autocomplete': 'off'
      }
    )
  )
  
  email = forms.EmailField(
    widget=forms.EmailInput(
      attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Enter Email Id',
        'autocomplete': 'off'
      }
    )
  )

  number = forms.CharField(
    label='Phone',
    widget=forms.TextInput(
      attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Enter Phone Number',
        'type': 'number',
        'autocomplete': 'off'
      }
    )
  )

  password1 = forms.CharField(
    label='Password',
    widget=forms.PasswordInput(
      attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Enter Password',
        'autocomplete': 'off'
      }
    )
  )

  password2 = forms.CharField(
    label='Confirm Password',
    widget=forms.PasswordInput(
      attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Confirm Password',
        'autocomplete': 'off'
      }
    )
  )

  class Meta:
    model = User
    fields = ('name','number','email','password1')

  def clean_email(self, *args, **kwargs):
    email = self.cleaned_data.get('email')
    qs = User.objects.filter(email=email)
    if qs.exists():
      raise forms.ValidationError('Email has already been registered!')
    else:
      return email

  def clean_password(self, *args, **kwargs):
    password1 = self.cleaned_data.get('password1')
    password2 = self.cleaned_data.get('password2')
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError('Passwords did not match!')
    else:
      return password2

  def clean_number(self,*args,**kwargs):
    phone = self.cleaned_data.get('number')
    qs = User.objects.filter(number=phone)
    if qs.exists():
      raise forms.ValidationError('Phone Number has already been registered!')
    else:
      return phone

  def save(self, commit=True):
    user = User(email=self.cleaned_data.get('email'),password=self.cleaned_data.get('password1'),name=self.cleaned_data.get('name'),number=self.cleaned_data.get('number'))
    # raise SystemExit
    if commit:
      user.save()
    return user


class LoginForm(forms.Form):
  number = forms.CharField(
    label='Phone',
    widget=forms.TextInput(
      attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Enter Phone Number',
        'type': 'number',
        'autocomplete': 'off'
      }
    )
  )
  password = forms.CharField(
    widget=forms.PasswordInput(
      attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Enter Password'
      }
    )
  )

  def clean(self, *args, **kwargs):
    number = self.cleaned_data.get('number')
    password = self.cleaned_data.get('password')
    qs = User.objects.filter(number=number)
    if not qs.exists():
      raise forms.ValidationError('User does not exist!')
    user_obj = qs.first()
    # print(user_obj.password)
    # raise SystemExit
    if  password!=user_obj.password:
      raise forms.ValidationError('Invalid Credentials!')
    self.cleaned_data['user_obj'] = user_obj
    return super(LoginForm, self).clean(*args, **kwargs)