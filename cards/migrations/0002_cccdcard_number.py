# Generated by Django 5.1.1 on 2024-10-22 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cccdcard',
            name='number',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]