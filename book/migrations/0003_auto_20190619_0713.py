# Generated by Django 2.2.1 on 2019-06-19 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20190619_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='main_genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='book.Category'),
        ),
    ]
