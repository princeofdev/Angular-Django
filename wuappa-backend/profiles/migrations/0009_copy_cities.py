# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations


def convert_city_to_array(apps, schema_editor):
    Profile = apps.get_model("profiles", "Profile")
    profiles = Profile.objects.all()
    for profile in profiles:
        if profile.city:
            profile.cities = [profile.city]
            profile.save()


class Migration(migrations.Migration):
    dependencies = [
        ('profiles', '0008_profile_cities'),
    ]

    operations = [
        migrations.RunPython(convert_city_to_array),
    ]
