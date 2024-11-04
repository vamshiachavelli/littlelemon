# Generated by Django 5.1.2 on 2024-11-04 21:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_menu_dish_of_the_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='DishOfTheDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.menu')),
            ],
        ),
        migrations.DeleteModel(
            name='SiteConfiguration',
        ),
    ]