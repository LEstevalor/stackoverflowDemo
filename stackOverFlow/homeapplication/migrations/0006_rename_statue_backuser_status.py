# Generated by Django 4.0.5 on 2023-08-29 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homeapplication', '0005_backuser_remove_followquestion_downvotes_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='backuser',
            old_name='statue',
            new_name='status',
        ),
    ]
