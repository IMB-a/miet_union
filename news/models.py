import os

from django.db import models
from django.utils import timezone
from django.dispatch import receiver

from miet_union.decorators import disable_for_loaddata


class News(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    main_text = models.TextField(verbose_name='Текст новости')
    image = models.FileField(
        upload_to="news/images", verbose_name='Изображение')
    created = models.DateTimeField(
        default=timezone.now, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created']


class EmailSubscription(models.Model):
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        error_messages={'unique': "This email has already been registered."}
    )
    created = models.DateTimeField(
        default=timezone.now, verbose_name='Дата подписки')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Почтовый адрес на рассылку'
        verbose_name_plural = 'Почтовые адреса на рассылку'
        ordering = ['-created']


# https://djangosnippets.org/snippets/10638/
def _get_model_filefield_names(model):
    return list(
        f.name for f in model._meta.get_fields() if isinstance(f, models.FileField)
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
