# Generated by Django 4.1.3 on 2022-11-20 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_delete_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('category_image', models.ImageField(upload_to='category')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='composition',
        ),
        migrations.RemoveField(
            model_name='product',
            name='prodapp',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category'),
        ),
    ]
