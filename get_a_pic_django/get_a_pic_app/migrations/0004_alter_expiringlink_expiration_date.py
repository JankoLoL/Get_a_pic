# Generated by Django 4.2.5 on 2023-10-05 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_a_pic_app', '0003_expiringlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiringlink',
            name='expiration_date',
            field=models.DateTimeField(null=True),
        ),
    ]