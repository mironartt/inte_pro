# Generated by Django 2.2.5 on 2019-10-13 12:48

import ckeditor_uploader.fields
import core.models.globals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_tile_is_availabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='BanckCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название банка полное')),
                ('short_name', models.CharField(max_length=100, verbose_name='Сокращенное название банка')),
                ('operating_account', models.CharField(max_length=50, verbose_name='Расчетный счет банка')),
                ('correspondent_account', models.CharField(max_length=50, verbose_name='Корреспондентский счет банка')),
                ('bic', models.CharField(max_length=50, verbose_name='Банковский идентификационный код (бик)')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Если необходимо описание')),
            ],
            options={
                'verbose_name': 'Карточка банка',
                'verbose_name_plural': 'Карточки банка',
            },
        ),
        migrations.CreateModel(
            name='ContactCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Заголовок')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('address', models.CharField(max_length=20, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=10, null=True, verbose_name='Географическая широта')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=10, null=True, verbose_name='Географическая длина')),
                ('is_availabled', models.BooleanField(default=True, verbose_name='Активна ли карточка')),
                ('is_copy', models.BooleanField(default=True, verbose_name='Включить кнопку “Скопировать”')),
                ('is_map', models.BooleanField(default=True, verbose_name='Включить Карту')),
                ('qr_image', models.ImageField(upload_to='contact_card_img', verbose_name='QR код')),
            ],
            options={
                'verbose_name': 'Карточка контактов',
                'verbose_name_plural': 'Карточки контактов',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=200, verbose_name='Тема сообщения, будет выбираться и настроек сайта')),
                ('title', models.CharField(max_length=500, verbose_name='Название проекта')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('text', models.TextField(verbose_name='Тело сообщения')),
                ('file', models.FileField(blank=True, null=True, upload_to=core.models.globals.generate_filename, verbose_name='Прикрепленный файл')),
            ],
            options={
                'verbose_name': 'Обращение пользователя',
                'verbose_name_plural': 'Обращения пользователя',
            },
        ),
        migrations.CreateModel(
            name='Requisites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Название компании')),
                ('inn', models.CharField(max_length=200, verbose_name='ИНН компании')),
                ('contacts', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Информация о компании')),
                ('file', models.FileField(blank=True, null=True, upload_to='requisites ', verbose_name='Прикрепленный файл')),
            ],
            options={
                'verbose_name': 'Реквизиты',
                'verbose_name_plural': 'Реквизиты',
            },
        ),
        migrations.CreateModel(
            name='SiteConf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_email', models.EmailField(max_length=254, verbose_name='Email для обратной связи')),
                ('topic', models.TextField(verbose_name='Темы сообщений обратной связи')),
                ('storage_link', models.CharField(max_length=200, verbose_name='Сылка на хранилище')),
            ],
            options={
                'verbose_name': 'Параметры сайта',
            },
        ),
        migrations.AlterField(
            model_name='project',
            name='main_image',
            field=models.ImageField(upload_to='project_img', verbose_name='Главное изображение Проекта'),
        ),
        migrations.AlterField(
            model_name='tile',
            name='is_availabled',
            field=models.BooleanField(default=False, verbose_name='Активна ли плитка'),
        ),
        migrations.AlterField(
            model_name='tile',
            name='main_image',
            field=models.ImageField(upload_to='tile_img', verbose_name='Главное изображение плитки'),
        ),
    ]
