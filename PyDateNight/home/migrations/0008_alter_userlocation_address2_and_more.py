# Generated by Django 5.0.4 on 2024-05-10 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_userlocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlocation',
            name='address2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userlocation',
            name='address3',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
