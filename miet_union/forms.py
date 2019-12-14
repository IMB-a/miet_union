import datetime

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from news.models import EmailSubscription


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
        initial='(пример) Иванов Иван Иванович',
        label='Фамилия, Имя, Отчество',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    group = forms.CharField(
        initial='(пример) БТС-10',
        label='Группа',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(
        initial='(пример) ул. Юности, 11, Зеленоград, Москва',
        label='Адрес проживания',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    reason = forms.CharField(
        initial='В связи с тяжелым материальным положением.',
        label='Причины, в силу которых необходимо оказание мат. помощи',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_and_month_of_last_request = forms.CharField(
        initial='(пример) 01.01',
        label='День и месяц последнего обращения',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    year_of_last_request = forms.CharField(
        initial='(пример) 1900',
        label='Год последнего обращения',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport_number_part_one = forms.CharField(
        initial='(пример) 0000',
        label='Серия паспорта',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport_number_part_two = forms.CharField(
        initial='(пример) 000000',
        label='Номер паспорта',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_issue = forms.DateField(
        initial=datetime.date(1900, 1, 1),
        label='Дата выдачи паспорта',
        widget=forms.DateInput(attrs={'class': 'form-control'}))
    place_of_issue = forms.CharField(
        initial='(пример) ГУ МВД РОССИИ ПО Г.МОСКВЕ',
        label='Место выдачи паспорта',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(
        min_length=11,
        max_length=11,
        initial='89950000000',
        label='Номер телефона',
        widget=forms.TextInput(attrs={'class': 'form-control'}))


class EmailingForm(forms.Form):
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'Электронная почта'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')

        if email and EmailSubscription.objects.filter(email=email):
            if EmailSubscription.objects.get(email=email):
                raise forms.ValidationError('Вы уже подписаны')
        return super(EmailingForm, self).clean(*args, **kwargs)


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

    def clean(self, *args, **kwargs):
        username = User.username
        current_password = self.cleaned_data.get('current_password')
        new_password = self.cleaned_data.get('new_password')
        confirmed_new_password = self.cleaned_data.get(
            'confirmed_new_password')
        if username and current_password:
            username = authenticate(username=username,
                                    password=current_password
                                    )
            # print(username)
            # if not username.check_password(current_password):
            #     raise forms.ValidationError('Неверный пароль')
        if new_password != confirmed_new_password:
            raise forms.ValidationError('Пароли не совпадают')
        return super(ChangePasswordForm, self).clean(*args, **kwargs)
