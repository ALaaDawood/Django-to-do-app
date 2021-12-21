# Generated by Django 3.2.7 on 2021-12-08 13:09

from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model("auth", "group")
    Permission = apps.get_model("auth", "permission")
    admin_group, created = Group.objects.get_or_create(name="admin_group")
    permissions = Permission.objects.filter(
        codename__in=["add_task", "change_task", "view_task", "delete_task"]
    )
    admin_group.permissions.set(permissions)
    normal_user_group, created = Group.objects.get_or_create(name="normal_user")
    permissions = Permission.objects.filter(codename__in=["view_task"])
    normal_user_group.permissions.set(permissions)


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0001_initial"),
    ]

    operations = [migrations.RunPython(create_groups)]
