# Generated by Django 5.1.2 on 2025-01-15 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_group_image_groupuser_points_groupuser_tasks_solved_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='unique_identifier',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
