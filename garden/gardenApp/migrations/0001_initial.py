# Generated by Django 3.2.7 on 2021-11-26 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PublicUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=64)),
                ('pass_hash', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=256)),
                ('verified', models.BooleanField(default=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ProduceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produce_name', models.CharField(max_length=64)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gardenApp.publicuser')),
            ],
        ),
        migrations.CreateModel(
            name='Produce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produce_name', models.CharField(max_length=64)),
                ('weight', models.FloatField()),
                ('fruits', models.BooleanField()),
                ('veggies', models.BooleanField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('image', models.ImageField(null=True, upload_to='produce_images')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gardenApp.publicuser')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('produce_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gardenApp.produce')),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gardenApp.publicuser')),
            ],
        ),
    ]
