# Generated by Django 4.2.6 on 2024-03-02 10:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("stopwatch", "0003_leaderboard"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Leaderboard",
        ),
    ]
