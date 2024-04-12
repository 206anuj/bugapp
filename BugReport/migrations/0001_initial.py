# Generated by Django 5.0.4 on 2024-04-09 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(max_length=64)),
                ('SDM', models.CharField(max_length=64)),
                ('issue_reported', models.CharField(max_length=512)),
                ('resolved_by', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]