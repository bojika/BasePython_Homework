from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.description


class ImportTopologyForm(forms.Form):
    # topology = MyModelChoiceField(queryset=Topology.objects.all())
    raw_data = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 20}))


class SelectTopologyForm(forms.Form):
    # topology = forms.ModelChoiceField(queryset=Topology.objects.all(),
    #                                   widget=forms.Select(attrs={'class':'form-select form-select-sm'}))
    topology = MyModelChoiceField(queryset=Topology.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-select form-select-sm',
                                                             'onchange': 'this.form.submit()'}))


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    class Meta:
         model = User
         fields = ('username', 'password')
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'form-control'


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        # widgets = {
        #     'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        #     'username': forms.TextInput(attrs={'class': 'form-input'})
        # }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'form-control'
    #         self.fields[field].widget.attrs['label'] =  None