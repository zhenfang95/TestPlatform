# Generated by Django 3.1 on 2021-03-24 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0011_db_host'),
    ]

    operations = [
        migrations.CreateModel(
            name='DB_project_host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=100, null=True)),
                ('des', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
