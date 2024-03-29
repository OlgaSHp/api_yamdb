# Generated by Django 3.2 on 2023-05-15 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="title",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="titles",
                to="reviews.category",
                verbose_name="атегория",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="confirmation_code",
            field=models.CharField(
                default="XXX",
                max_length=255,
                null=True,
                verbose_name="код подтверждения",
            ),
        ),
    ]
