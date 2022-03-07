# Generated by Django 4.0.1 on 2022-03-06 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_shop_display_picture'),
        ('order', '0003_alter_order_from_user_id_alter_orderitems_to_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordercustom',
            old_name='option',
            new_name='value',
        ),
        migrations.AddField(
            model_name='ordercustom',
            name='shop_custom_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.shopcustom'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ordercustom',
            name='type',
            field=models.TextField(),
        ),
    ]