# Generated by Django 3.2.7 on 2021-11-27 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gardenApp', '0006_alter_publicuser_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1', to='gardenApp.publicuser')),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2', to='gardenApp.publicuser')),
            ],
        ),
        migrations.AlterField(
            model_name='produce',
            name='image',
            field=models.ImageField(default='produce_images/default_produce.jpg', upload_to='produce_images'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField(auto_created=True)),
                ('msg', models.TextField()),
                ('chatID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gardenApp.chat')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gardenApp.publicuser')),
            ],
        ),
    ]
