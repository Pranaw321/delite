# Generated by Django 4.1.4 on 2023-02-02 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurants', '0002_remove_restorent_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=10)),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('desc', models.CharField(max_length=255, null=True)),
                ('slug', models.CharField(max_length=255, null=True)),
                ('recipe', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('veg', 'Veg'), ('nonveg', 'Nonveg'), ('vegan', 'Vegan')], default='veg', max_length=10)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menus.category')),
            ],
        ),
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menus.item')),
            ],
        ),
        migrations.CreateModel(
            name='AddsOn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menus.item')),
            ],
        ),
    ]