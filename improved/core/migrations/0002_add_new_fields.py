from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='teams/'),
        ),
        migrations.AlterField(
            model_name='news',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='news/'),
        ),
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
