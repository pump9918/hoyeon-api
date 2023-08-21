# Generated by Django 4.2.4 on 2023-08-21 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ttsposts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ttspost',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ttspost',
            name='tts_audio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ttsposts.ttsaudio'),
        ),
        migrations.AddField(
            model_name='ttspost',
            name='tts_title_audio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ttsposts.ttsaudiotitle'),
        ),
        migrations.AddField(
            model_name='ttsaudiotitle',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ttsaudio',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
