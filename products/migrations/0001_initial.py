# Generated by Django 4.0.4 on 2022-05-12 21:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
