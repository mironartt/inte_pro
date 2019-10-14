import os
import time

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from solo.models import SingletonModel



class SiteConf(SingletonModel):

    class Meta:
        verbose_name = 'Параметры сайта'

    feedback_email = models.EmailField('Email для обратной связи')
    # topic = models.TextField(verbose_name='Темы сообщений обратной связи')
    storage_link = models.CharField(max_length=200, verbose_name='Сылка на хранилище')


class Tile(models.Model):

    class Meta:
        verbose_name = 'Плитка'
        verbose_name_plural = 'Плитки'

    TYPE = (
        ('projects', 'Проекты',),
        ('contacts', 'Контакты'),
        ('storage', 'Облачное хранилище'),
        ('requisites', 'Реквизиты'),
    )

    type = models.CharField(max_length=50, verbose_name='Тип плитки', choices=TYPE)
    title = models.CharField(max_length=100, verbose_name='Заголовок плитки (отображается при наведение на нее во всплывающем)')
    main_image = models.ImageField(upload_to='tile_img', verbose_name='Главное изображение плитки')
    description = models.CharField(max_length=130, verbose_name='Описание плитки')
    is_availabled = models.BooleanField(default=False, verbose_name='Активна ли плитка')

    def __str__(self):
        return '(id:{0}) {1} - {2}'.format(self.id, self.type, self.title)

    def get_type(self):
        return [i for i in Tile.TYPE if self.type == i[0]][0][1]


class Project(models.Model):

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    tile = models.ForeignKey(Tile, on_delete=models.CASCADE, verbose_name='Плитка к которой относится', related_name='tile', null=True)
    title = models.CharField(max_length=500, verbose_name='Название проекта')
    # main_image = models.ImageField(upload_to='project_img', verbose_name='Главное изображение Проекта')
    latitude = models.DecimalField('Географическая широта', max_digits=10, decimal_places=6, null=True)
    longitude = models.DecimalField('Географическая длина', max_digits=10, decimal_places=6, null=True)
    description = RichTextUploadingField(verbose_name='Описание на главной странице')

    def __str__(self):
        return '(id:{0}) {1}{2}'.format(self.id, self.title, ' - {0}/{1}'.format(self.latitude, self.longitude) if self.latitude and self.longitude else '')


class ContactCard(models.Model):

    class Meta:
        verbose_name = 'Карточка контактов'
        verbose_name_plural = 'Карточки контактов'

    title = models.CharField(max_length=500, verbose_name='Заголовок')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    latitude = models.DecimalField('Географическая широта', max_digits=10, decimal_places=6, null=True)
    longitude = models.DecimalField('Географическая длина', max_digits=10, decimal_places=6, null=True)
    is_availabled = models.BooleanField(default=True, verbose_name='Активна ли карточка')
    is_copy = models.BooleanField(default=True, verbose_name='Включить кнопку “Скопировать”')
    is_map = models.BooleanField(default=True, verbose_name='Включить Карту')
    qr_image = models.ImageField(upload_to='contact_card_img', verbose_name='QR код')

    def __str__(self):
        return '(id:{0}) {1}'.format(self.id, self.title)


class Topic(models.Model):

    class Meta:
        verbose_name = 'Тема для обращения в обратной связи'
        verbose_name_plural = 'Темы для обращения в обратной связи'

    title = models.CharField(max_length=500, verbose_name='Тема')

    def __str__(self):
        return '(id:{0}) {1}'.format(self.id, self.title)


def generate_filename(instance, filename):
    filename = str(time.time())[6:8] + str(time.time())[11:14] + filename
    return 'feedback_img/{0}'.format(filename)


class Feedback(models.Model):

    class Meta:
        verbose_name = 'Обращение пользователя'
        verbose_name_plural = 'Обращения пользователя'

    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING, verbose_name='Тема сообщения, будет выбираться и настроек сайта')
    title = models.CharField(max_length=500, verbose_name='Название проекта')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    text = models.TextField(verbose_name='Тело сообщения')
    file = models.FileField(upload_to=generate_filename, verbose_name='Прикрепленный файл', null=True, blank=True)

    def __str__(self):
        return '(id:{0}) {1}'.format(self.id, self.title)


class BanckCard(models.Model):
    class Meta:
        verbose_name = 'Карточка банка'
        verbose_name_plural = 'Карточки банка'

    name = models.CharField(max_length=500, verbose_name='Название банка полное')
    short_name = models.CharField(max_length=100, verbose_name='Сокращенное название банка')
    operating_account = models.CharField(max_length=50, verbose_name='Расчетный счет банка')
    correspondent_account = models.CharField(max_length=50, verbose_name='Корреспондентский счет банка')
    bic = models.CharField(max_length=50, verbose_name='Банковский идентификационный код (бик)')
    description = RichTextUploadingField(verbose_name='Если необходимо описание')

    def __str__(self):
        return '(id:{0}) {1}'.format(self.id, self.short_name)


class Requisites(models.Model):

    class Meta:
        verbose_name = 'Реквизиты'
        verbose_name_plural = 'Реквизиты'

    title = models.CharField(max_length=500, verbose_name='Название компании')
    inn = models.CharField(max_length=200, verbose_name='ИНН компании')
    contacts = RichTextUploadingField(verbose_name='Информация о компании')
    file = models.FileField(upload_to='requisites ', verbose_name='Прикрепленный файл', null=True, blank=True)

    def __str__(self):
        return '(id:{0}) {1}'.format(self.id, self.title)
