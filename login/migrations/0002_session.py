# Generated by Django 3.0.1 on 2019-12-29 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('browser_family', models.TextField()),
                ('browser_version', models.TextField()),
                ('ip', models.GenericIPAddressField()),
                ('device', models.TextField()),
                ('system_family', models.TextField()),
                ('system_version', models.TextField()),
                ('mobile', models.BooleanField()),
                ('tablet', models.BooleanField()),
                ('touch_capable', models.BooleanField()),
                ('pc', models.BooleanField()),
                ('bot', models.BooleanField()),
                ('meta', models.TextField()),
            ],
        ),
    ]
