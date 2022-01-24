# Generated by Django 4.0 on 2022-01-20 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(blank=True, max_length=255, null=True)),
                ('document_front', models.ImageField(blank=True, null=True, upload_to='document')),
                ('document_back', models.ImageField(blank=True, null=True, upload_to='document')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='document')),
            ],
        ),
    ]