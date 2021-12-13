# Generated by Django 4.0 on 2021-12-13 05:35

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('developer', '0002_developer_created_on_developer_updated_on'),
        ('project', '0005_project_created_on_project_updated_on_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='additional_development',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_estimate', jsonfield.fields.JSONField()),
                ('new_estimate', jsonfield.fields.JSONField()),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='developer.developer')),
            ],
        ),
    ]
