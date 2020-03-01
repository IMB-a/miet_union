import logging
import os
import random
import string

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, identify_hasher
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from miet_union.decorators import disable_for_loaddata
from miet_union import settings

_ascii = string.ascii_uppercase + string.ascii_lowercase + string.digits


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, first_name=None, middle_name=None,
                    last_name=None, password=None, is_active=None,
                    is_staff=None, is_admin=None):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('Пользователь должен иметь электронную почту')
        if not password:
            raise ValueError('Пользователь должен иметь пароль')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          first_name=first_name,
                          middle_name=middle_name,
                          last_name=last_name)
        user.set_password(password)
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password,
                                is_staff=True, is_admin=True)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(email, password=password,
                                is_staff=True, is_admin=False)
        return user


class User(AbstractBaseUser):
    """

    """
    status_choices = [
        ('no_info', 'Нет информации'),
        ('in_progress', 'На рассмотрении'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена')
    ]
    last_name = models.CharField(
        _('last name'), max_length=255, blank=True, null=True)
    first_name = models.CharField(
        _('first name'), max_length=255, blank=True, null=True)
    middle_name = models.CharField(
        verbose_name='Отчество', max_length=255, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    financial_assistance_status = models.CharField(
        max_length=250,
        default='no_info',
        choices=status_choices,
        verbose_name='Статус по оформлению материальной помощи'
    )
    secret_key = models.CharField(
        max_length=30,
        verbose_name='Секретный ключ',
        help_text='''Случайно сгерерованный ключ при сознании сущности
        длинной в 30 символов.''',
        default=''.join(
            random.choice(_ascii) for _ in range(30))
    )
    is_account_confirmed = models.BooleanField(
        verbose_name='Аккаунт продтвержден',
        default=False
    )
    is_email_subscription_confirmed = models.BooleanField(
        verbose_name='Подписка на рассылку подтверждена',
        default=False
    )
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-last_name']

    def __str__(self):
        return self.email

    def get_short_name(self):
        """Return the short name for the user."""
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.email

    def get_full_name(self):
        """
        Return the first_name, middle_name and last_name, with a space
        in between.
        """
        if self.first_name and self.last_name:
            return f'''{self.first_name}
            {self.middle_name} {self.last_name}'''.strip()
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class CommissionsOfProfcom(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    file = models.FileField(
        upload_to="documents/", verbose_name='Файл')

    def __str__(self):
        """Return CommissionsOfProfcom title"""
        return self.title

    class Meta:
        verbose_name = 'Комиссии профкома'
        verbose_name_plural = 'Комиссии профкома'
        ordering = ['title']


class EmailSubscription(models.Model):
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        error_messages={'unique': "This email has already been registered."}
    )
    secret_key = models.CharField(
        max_length=30,
        verbose_name='Секретный ключ',
        help_text='''Случайно сгерерованный ключ при сознании сущности
        длинной в 30 символов.''',
        default=''.join(
            random.choice(_ascii) for _ in range(30))
    )
    is_confirmed = models.BooleanField(
        verbose_name='Подтверждена',
        default=False
    )
    created = models.DateTimeField(
        default=timezone.now, verbose_name='Дата подписки')

    def __str__(self):
        """Return EmailSubscription email"""
        return self.email

    class Meta:
        verbose_name = 'Почтовый адрес на рассылку'
        verbose_name_plural = 'Почтовые адреса на рассылку'
        ordering = ['-created']


class News(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    main_text = models.TextField(verbose_name='Текст новости')
    image = models.FileField(
        upload_to="news/images",
        verbose_name='Изображение',
        help_text='''Рекомендация: изображение должно быть
        в горизонтальной форме, в идеале в формате 16:9''')
    created = models.DateTimeField(
        default=timezone.now, verbose_name='Дата создания')

    def __str__(self):
        """Return News title"""
        return self.title

    @staticmethod
    def search_news(str_input):
        """
        Return instances with filter if exists
        """
        title_res = News.objects.none()
        main_text_res = News.objects.none()
        if News.objects.filter(title__contains=str_input):
            title_res = News.objects.filter(title__contains=str_input)
        if News.objects.filter(main_text__contains=str_input):
            main_text_res = News.objects.filter(main_text__contains=str_input)
        return title_res, main_text_res

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created']


class HelpForProforg(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    file = models.FileField(
        upload_to="documents/", verbose_name='Файл')

    def __str__(self):
        """Return HelpForProforg title"""
        return self.title

    class Meta:
        verbose_name = 'В помощь профоргу'
        verbose_name_plural = 'В помощь профоргу'
        ordering = ['title']


class HelpForStudentProforg(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    file = models.FileField(
        upload_to="documents/", verbose_name='Файл')

    def __str__(self):
        """Return HelpForStudentProforg title"""
        return self.title

    class Meta:
        verbose_name = 'В помощь студенческому профоргу'
        verbose_name_plural = 'В помощь студенческому профоргу'
        ordering = ['title']


class TheMainActivitiesOfProforg(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    file = models.FileField(
        upload_to="documents/", verbose_name='Файл')

    def __str__(self):
        """Return TheMainActivitiesOfProforg title"""
        return self.title

    class Meta:
        verbose_name = 'Основные направления деятельности профорга'
        verbose_name_plural = 'Основные направления деятельности профорга'
        ordering = ['title']


class ProtectionOfPersonalInformation(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    file = models.FileField(
        upload_to="documents/", verbose_name='Файл')

    def __str__(self):
        """Return ProtectionOfPersonalInformation title"""
        return self.title

    class Meta:
        verbose_name = 'Защита персональных данных'
        verbose_name_plural = 'Защита персональных данных'
        ordering = ['title']


class NormativeDocuments(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    file = models.FileField(
        upload_to="documents/", verbose_name='Файл')

    def __str__(self):
        """Return NormativeDocuments title"""
        return self.title

    class Meta:
        verbose_name = 'Законодательные, нормативные и уставные документы'
        verbose_name_plural = '''Законодательные,
                                 нормативные и уставные документы'''
        ordering = ['title']


class UsefulLinks(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    file = models.FileField(
        upload_to="documents/", verbose_name='Файл')

    def __str__(self):
        """Return UsefulLinks title"""
        return self.title

    class Meta:
        verbose_name = 'Полезные ссылки'
        verbose_name_plural = 'Полезные ссылки'
        ordering = ['title']


class Worker(models.Model):
    first_name = models.CharField(
        max_length=100, verbose_name='Имя', null=True)
    last_name = models.CharField(
        max_length=100, verbose_name='Фамилия', null=True)
    middle_name = models.CharField(
        max_length=100, verbose_name='Отчество', null=True)
    position = models.CharField(max_length=100, verbose_name="Должность")
    phone_num = models.CharField(max_length=11, verbose_name='Номер телефона')
    email = models.EmailField(max_length=254, verbose_name='Электронная почта')
    photo = models.ImageField(
        upload_to="workers/images", verbose_name='Фото')

    def __str__(self):
        """Return Worker first_name"""
        return self.first_name

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'
        ordering = ['last_name']


class MoneyHelp(models.Model):
    status_choices = [
        ('no_info', 'Нет информации'),
        ('in_progress', 'На рассмотрении'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена')
    ]
    rank_choices = [
        ('student', 'Студент'),
        ('graduate_student', 'Аспирант'),
        ('worker', 'Сотрудник')
    ]
    first_name = models.CharField(max_length=250, verbose_name='Имя')
    middle_name = models.CharField(max_length=250, verbose_name='Отчество')
    last_name = models.CharField(max_length=250, verbose_name='Фамилия')
    status = models.CharField(
        max_length=250,
        default='no_info',
        choices=status_choices,
        verbose_name='Статус'
    )
    rank = models.CharField(
        max_length=250,
        default='no_info',
        choices=rank_choices,
        verbose_name='Студент, Аспирант или Сотрудник'
    )

    def __str__(self):
        """Return MoneyHelp first_name"""
        return self.first_name

    class Meta:
        verbose_name = 'Материальная помощь'
        verbose_name_plural = 'Материальная помощь'
        ordering = ['last_name']


# https://djangosnippets.org/snippets/10638/
def _get_model_filefield_names(model):
    """
    Get model filefield names for auto_delete_file_on_delete func
    """
    return list(
        f.name for f in model._meta.get_fields() if isinstance(
            f,
            models.FileField
        )
    )


@receiver(models.signals.post_delete, sender=News)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """

    model_filefield_names = _get_model_filefield_names(sender)

    for field in model_filefield_names:
        f = getattr(instance, field)
        if f and os.path.isfile(f.path):
            os.remove(f.path)


@receiver(models.signals.pre_save, sender=News)
@disable_for_loaddata
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    model_filefield_names = _get_model_filefield_names(sender)
    file_fields = list(f for f in kwargs.get(
        'update_fieds') or [] if f in model_filefield_names)

    for field in file_fields:
        try:
            old_file = getattr(sender.objects.get(pk=instance.pk), field)
        except sender.DoesNotExist:
            continue

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(models.signals.pre_save, sender=News)
def send_emails_when_news_pre_save(instance, *args, **kwargs):
    """
    Send email to all user emails in db when
    new news is created
    """
    all_emails = EmailSubscription.objects.all()
    send_email(instance, all_emails)


logger = logging.getLogger(__name__)


def send_email(instance, all_emails):
    """
    Send email to all user emails in db
    """
    context = {'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
               'instance': instance}
    all_email_addr = []
    for addr in all_emails:
        if addr.is_confirmed is True:
            all_email_addr.append(addr.email)
            try:
                email_instance = EmailSubscription.objects.get(
                    email=addr.email)
                context.update({'secret_key': email_instance.secret_key})
                send_mail(
                    subject='Новоя новость на сайте профкома института МИЭТ',
                    message='Hello from django.',
                    html_message=render_to_string(
                        'miet_union/mail_template.html', context),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=all_email_addr,
                    fail_silently=False,
                )
            except NameError:
                logger.error('EMAIL_HOST_USER not found in send_email() ')
