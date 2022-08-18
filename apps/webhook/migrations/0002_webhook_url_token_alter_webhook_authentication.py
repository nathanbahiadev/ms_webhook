# Generated by Django 4.1 on 2022-08-17 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='webhook',
            name='url_token',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='webhook',
            name='authentication',
            field=models.CharField(choices=[('0', 'No authentication'), ('1', 'Basic authentication'), ('2', 'JWT authentication'), ('3', 'API Key authentication')], default='0', max_length=1),
        ),
    ]