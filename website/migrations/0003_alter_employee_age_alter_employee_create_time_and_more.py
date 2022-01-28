# Generated by Django 4.0.1 on 2022-01-19 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_employee_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='age',
            field=models.IntegerField(blank=True, null=True, verbose_name='Age'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='create_time',
            field=models.DateTimeField(verbose_name='Create Time'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='dept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.department', verbose_name='Department'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.SmallIntegerField(choices=[(1, 'F'), (2, 'M')], verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(max_length=16, verbose_name='Name'),
        ),
    ]