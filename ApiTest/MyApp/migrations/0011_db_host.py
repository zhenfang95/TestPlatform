# Generated by Django 3.1 on 2021-03-24 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0010_db_step_public_header'),
    ]

    operations = [
        migrations.CreateModel(
            name='DB_host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=100, null=True)),
                ('des', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
