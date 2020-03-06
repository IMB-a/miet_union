from django import forms


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


class EmailingForm(forms.Form):
    email = forms.EmailField(
        required=False,
        label='EmailingForm',
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'Электронная почта'}))


class EmailingUnsubscribeForm(forms.Form):
    email = forms.EmailField(
        required=False,
        label='EmailingUnsubscribeForm',
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'Электронная почта'}))


class SearchNewsForm(forms.Form):
    str_input = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Ключевые слова'}))


class UserLoginForm(forms.Form):
    email = forms.CharField(
        label='Электронная почта',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegistrationForm(forms.Form):
    rank_choices = [
        ('student', 'Студент'),
        ('graduate_student', 'Аспирант'),
        ('worker', 'Сотрудник')
    ]
    email = forms.EmailField(
        required=False,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'Электронная почта'}))
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirmed_password = forms.CharField(
        label='Повторный пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    rank = forms.ChoiceField(
        label='Кем являетесь',
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=rank_choices)
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(
        label='Отчество',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
