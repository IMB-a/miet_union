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
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
