# Generated by Django 3.2.7 on 2021-09-04 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='reason_for_application',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
