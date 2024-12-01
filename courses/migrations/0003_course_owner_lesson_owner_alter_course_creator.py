# Generated by Django 4.2 on 2024-11-24 08:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0002_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owned_courses', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='owner',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='owned_lessons', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_courses', to=settings.AUTH_USER_MODEL, verbose_name='Создатель'),
        ),
    ]
