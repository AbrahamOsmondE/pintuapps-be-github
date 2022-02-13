# Generated by Django 4.0.1 on 2022-02-04 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('shop_item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shopitem')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartCustom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('user', 'user'), ('text', 'text'), ('dropdown', 'dropdown')], max_length=100)),
                ('option', models.TextField()),
                ('cart_item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.cartitem')),
            ],
        ),
    ]
