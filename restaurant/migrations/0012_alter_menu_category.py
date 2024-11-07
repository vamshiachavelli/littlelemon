# Generated by Django 5.1.2 on 2024-11-07 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0011_alter_menu_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='category',
            field=models.CharField(blank=True, choices=[('appetizer', 'Appetizer'), ('main_course', 'Main Course'), ('dessert', 'Dessert'), ('beverage', 'Beverage')], max_length=20, null=True),
        ),
    ]
