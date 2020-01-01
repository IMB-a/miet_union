import datetime

from django import forms
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Такого пользователя нет')
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class StudentMoneyForm(forms.Form):
    full_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Фамилия, Имя, Отчество'}))
    group = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Группа'}))
    address = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Адрес проживания'}))
    reason = forms.CharField(
        label='',
        initial='В связи с тяжелым материальным положением.',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Причины, в силу которых необходимо оказание мат. помощи'}))
    date_and_month_of_last_request = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'День и месяц последнего обращения'}))
    year_of_last_request = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Год последнего обращения'}))
    passport_number_part_one = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Серия паспорта'}))
    passport_number_part_two = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Номер паспорта'}))
    date_of_issue = forms.DateField(
        label='',
        widget=forms.DateInput(attrs={'class': 'form-control',
                                      'placeholder': 'Дата выдачи паспорта'}))
    place_of_issue = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Место выдачи паспорта'}))
    phone_number = forms.CharField(
        label='',
        min_length=11,
        max_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Номер телефона'}))


class EmailingForm(forms.Form):
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'Электронная почта'}))


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirmed_new_password = forms.CharField(
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
