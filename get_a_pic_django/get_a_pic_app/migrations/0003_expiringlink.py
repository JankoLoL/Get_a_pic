# Generated by Django 4.2.5 on 2023-10-05 08:32

from django.db import migrations, models
import django.db.models.deletion
import secrets


class Migration(migrations.Migration):

    dependencies = [
        ('get_a_pic_app', '0002_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpiringLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(default=secrets.token_urlsafe, max_length=50, unique=True)),
                ('expiration_date', models.DateTimeField()),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='get_a_pic_app.image')),
            ],
        ),
    ]
