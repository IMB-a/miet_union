from django.db import models


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
