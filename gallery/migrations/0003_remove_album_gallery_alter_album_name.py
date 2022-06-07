# Generated by Django 4.0 on 2022-04-02 10:46

from django.db import migrations, models
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_remove_album_user_remove_image_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='gallery',
        ),
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.CharField(default=1, help_text='Name of the album. Must be unique.', max_length=1024, unique=True, validators=[gallery.models.validate_album_name], verbose_name='Name'),
            preserve_default=False,
        ),
    ]
