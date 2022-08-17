# Generated by Django 4.1 on 2022-08-17 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('url', models.URLField()),
                ('identifier', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('json_data', models.TextField(blank=True, null=True)),
                ('sending_attempts', models.PositiveIntegerField(default=0)),
                ('sended', models.BooleanField(default=False)),
                ('failed', models.BooleanField(default=False)),
                ('return_from_receiver_text', models.TextField(blank=True, null=True)),
                ('return_from_receiver_json', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='webhooks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Errors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.PositiveIntegerField(blank=True, null=True)),
                ('error_type', models.CharField(blank=True, max_length=255, null=True)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('webhook', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='logs', to='webhook.webhook')),
            ],
        ),
    ]
