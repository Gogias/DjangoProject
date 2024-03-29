# Generated by Django 2.1.4 on 2019-04-09 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20190330_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='files',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Project'),
        ),
    ]
