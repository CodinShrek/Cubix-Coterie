# Generated by Django 4.2.6 on 2024-03-02 10:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("community", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="communitychat",
            old_name="owner",
            new_name="User",
        ),
    ]
