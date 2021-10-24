# Generated by Django 3.2.7 on 2021-10-23 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('date', models.DateField()),
                ('author', models.CharField(max_length=64)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CorpUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('pass_hash', models.CharField(max_length=256)),
                ('address', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProduceAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PublicUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=256)),
                ('pass_hash', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='ProduceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produce_name', models.CharField(max_length=256)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('corp_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gardenApp.corpuser')),
            ],
        ),
        migrations.CreateModel(
            name='Produce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produce_name', models.CharField(max_length=256)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gardenApp.publicuser')),
            ],
        ),
    ]
