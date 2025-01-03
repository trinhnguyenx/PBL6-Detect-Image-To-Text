# Generated by Django 5.1.1 on 2024-12-25 11:12

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BHYTCard',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.CharField(blank=True, max_length=255, null=True)),
                ('expire_date', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('is_valid', models.BooleanField(default=False)),
                ('images', models.CharField(blank=True, max_length=255, null=True)),
                ('ihos', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, max_length=255, null=True)),
                ('iplace', models.CharField(blank=True, max_length=255, null=True)),
                ('issue_date', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bhyt_cards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('user', 'id'), name='unique_user_bhyt_card')],
            },
        ),
        migrations.CreateModel(
            name='CCCDCard',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.CharField(blank=True, max_length=255, null=True)),
                ('expire_date', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('is_valid', models.BooleanField(default=False)),
                ('images', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, max_length=255, null=True)),
                ('origin_place', models.CharField(blank=True, max_length=255, null=True)),
                ('current_place', models.CharField(blank=True, max_length=255, null=True)),
                ('issue_date', models.CharField(blank=True, max_length=255, null=True)),
                ('nationality', models.CharField(blank=True, max_length=255, null=True)),
                ('personal_identifi', models.CharField(default='', max_length=255)),
                ('images_behind', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cccd_cards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('user', 'id'), name='unique_user_cccd_card')],
            },
        ),
        migrations.CreateModel(
            name='GPLXCard',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.CharField(blank=True, max_length=255, null=True)),
                ('expire_date', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('is_valid', models.BooleanField(default=False)),
                ('images', models.CharField(blank=True, max_length=255, null=True)),
                ('level', models.CharField(blank=True, max_length=255, null=True)),
                ('iplace', models.CharField(blank=True, max_length=255, null=True)),
                ('origin_place', models.CharField(blank=True, max_length=255, null=True)),
                ('issue_date', models.CharField(blank=True, max_length=255, null=True)),
                ('nationality', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='gplx_cards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('user', 'id'), name='unique_user_gplx_card')],
            },
        ),
    ]
