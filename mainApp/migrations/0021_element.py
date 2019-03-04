# Generated by Django 2.1.1 on 2018-09-28 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0020_auto_20180920_2001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calorie', models.FloatField(default=0)),
                ('carbohydrate', models.FloatField(default=0)),
                ('fat', models.FloatField(default=0)),
                ('protein', models.FloatField(default=0)),
                ('cellulose', models.FloatField(default=0)),
                ('vitaminA', models.FloatField(default=0)),
                ('vitaminB1', models.FloatField(default=0)),
                ('vitaminB2', models.FloatField(default=0)),
                ('vitaminB6', models.FloatField(default=0)),
                ('vitaminC', models.FloatField(default=0)),
                ('vitaminE', models.FloatField(default=0)),
                ('carotene', models.FloatField(default=0)),
                ('cholesterol', models.FloatField(default=0)),
                ('Mg', models.FloatField(default=0)),
                ('Ca', models.FloatField(default=0)),
                ('Fe', models.FloatField(default=0)),
                ('Zn', models.FloatField(default=0)),
                ('Cu', models.FloatField(default=0)),
                ('Mn', models.FloatField(default=0)),
                ('K', models.FloatField(default=0)),
                ('P', models.FloatField(default=0)),
                ('Na', models.FloatField(default=0)),
                ('Se', models.FloatField(default=0)),
            ],
        ),
    ]
