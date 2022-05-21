# Generated by Django 4.0 on 2022-04-03 16:32

from django.db import migrations, models
import django.db.models.deletion
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_rename_gallary_album_gallery_album_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='gallery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='gallery.gallery'),
        ),
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.CharField(help_text='Name of the album. Must be unique.', max_length=1024, validators=[gallery.models.validate_album_name], verbose_name='Name'),
        ),
    ]