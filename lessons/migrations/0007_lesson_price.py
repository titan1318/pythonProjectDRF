# Generated by Django 4.2.5 on 2024-12-01 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0006_course_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Цена'),
        ),
    ]
