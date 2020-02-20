import logging
import os
import random
import string

from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone

from miet_union.decorators import disable_for_loaddata
from miet_union import settings

_ascii = string.ascii_uppercase + string.ascii_lowercase + string.digits


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
        default=''.join(
            random.choice(_ascii) for _ in range(30))
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
        upload_to="news/images", verbose_name='Изображение')
    created = models.DateTimeField(
        default=timezone.now, verbose_name='Дата создания')

    def __str__(self):
        """Return News title"""
        return self.title

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
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество')
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
def send_emails(instance, *args, **kwargs):
    """
    Send email to all user emails in db when
    new news is created
    """
    print('pre_save send_emails')
    all_emails = EmailSubscription.objects.all()
    send_email(instance, all_emails)


logger = logging.getLogger(__name__)


def send_email(instance, all_emails):
    """
    Send email to all user emails in db
    """
    context = {'ALLOWED_HOSTS': settings.ALLOWED_HOSTS, }
    context.update({'instance': instance})
    all_email_addr = []
    for addr in all_emails:
        all_email_addr.append(addr.email)
        try:
            email_instance = EmailSubscription.objects.get(email=addr.email)
            context.update({'secret_key': email_instance.secret_key})
            send_mail(
                subject='Новоя новость на сайте профкома института МИЭТ',
                message='Hello from django.',
                # render with dynamic value
                html_message=render_to_string(
                    'miet_union/mail_template.html', context),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=all_email_addr,
                # recipient_list=list(addr.email),
                fail_silently=False,
            )
            logger.info('Письмо отправляется ')
            print('Письмо отправляется ')
        except NameError:
            logger.error('EMAIL_HOST_USER not found in send_email() ')
