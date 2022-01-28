from attr import fields
import django
from website import models
from django import forms
from website.utils.encrypt import md5


class BootStrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs = {"class":"form-control"}

class UserModelForm(BootStrapModelForm):
    class Meta:
        model = models.Employee
        fields = ['name', 'age', 'dept', 'gender', 'create_time']

class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    class Meta:
        model = models.Admin
        fields = ['user_name', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm_pwd = md5(self.cleaned_data.get('confirm_password'))
        
        if pwd != confirm_pwd:
            raise django.core.exceptions.ValidationError('Password is not same')

        return confirm_pwd

class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['user_name']

class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = models.Admin
        fields = ['password']
        widgets = {
            'password': forms.PasswordInput
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        same = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if same:
            raise django.core.exceptions.ValidationError('Password can\'t same as previous one!')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm_pwd = md5(self.cleaned_data.get('confirm_password'))
        
        if pwd != confirm_pwd:
            raise django.core.exceptions.ValidationError('Password is not same')

        return confirm_pwd

class LoginModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['user_name', 'password']
        widgets = {
            'password': forms.PasswordInput
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        same = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if same:
            raise django.core.exceptions.ValidationError('Password can\'t same as previous one!')
        return md5(pwd)

