# Generated by Django 4.1.5 on 2023-01-18 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adminlog',
            fields=[
                ('User_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('Password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Animalnum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Animalname', models.CharField(max_length=50)),
                ('Rate', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Disaster_amount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Affectedno', models.IntegerField()),
                ('Applicationno', models.IntegerField()),
                ('Amount', models.IntegerField()),
                ('Depreciation', models.IntegerField()),
                ('Status', models.CharField(max_length=11, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Disasterfloor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Floor', models.CharField(max_length=50)),
                ('Rate', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Disasterroof',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Roof', models.CharField(max_length=50)),
                ('Rate', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Dismanagereg',
            fields=[
                ('Name', models.CharField(max_length=50)),
                ('Address', models.CharField(max_length=50)),
                ('District', models.CharField(max_length=50)),
                ('Mobno', models.BigIntegerField()),
                ('Email_id', models.CharField(max_length=50)),
                ('user_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('Password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Eventname', models.CharField(max_length=50)),
                ('Description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Productamount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Productname', models.CharField(max_length=50)),
                ('Rate', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Userreg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Address', models.CharField(max_length=50)),
                ('Contactno', models.BigIntegerField()),
                ('Email_id', models.CharField(max_length=50)),
                ('Aadhaarno', models.BigIntegerField()),
                ('Village', models.CharField(max_length=50)),
                ('User_id', models.CharField(max_length=50)),
                ('Password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='villagereg',
            fields=[
                ('Name', models.CharField(max_length=50)),
                ('Address', models.CharField(max_length=50)),
                ('Contactno', models.BigIntegerField()),
                ('Village', models.CharField(max_length=50)),
                ('Block', models.CharField(max_length=50)),
                ('District', models.CharField(max_length=50)),
                ('User_id', models.CharField(max_length=50)),
                ('Password', models.CharField(max_length=50)),
                ('Officer_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Email_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Userpersonal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Taluk', models.CharField(max_length=50)),
                ('Surveyno', models.IntegerField()),
                ('Bankname', models.CharField(max_length=100)),
                ('Bankbranch', models.CharField(max_length=50)),
                ('Accno', models.BigIntegerField()),
                ('Applicationno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dces.userreg')),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('Houseno', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('Area', models.CharField(max_length=50)),
                ('Floor', models.CharField(max_length=50)),
                ('Roof', models.CharField(max_length=50)),
                ('Staircase', models.CharField(max_length=50)),
                ('Diprecition', models.CharField(max_length=50)),
                ('Status', models.CharField(max_length=50, null=True)),
                ('Sqfeet', models.CharField(max_length=50)),
                ('Housephoto', models.CharField(max_length=100, null=True)),
                ('Reason', models.CharField(max_length=255, null=True)),
                ('Applicationno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dces.userreg')),
            ],
        ),
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('Farmno', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('Area', models.CharField(max_length=50)),
                ('Animalname', models.CharField(max_length=50)),
                ('Animalfood', models.CharField(max_length=50)),
                ('Numofanimal', models.IntegerField()),
                ('Status', models.CharField(max_length=50, null=True)),
                ('Farmphoto', models.CharField(max_length=100, null=True)),
                ('Reason', models.CharField(max_length=255, null=True)),
                ('Applicationno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dces.userreg')),
            ],
        ),
        migrations.CreateModel(
            name='Agriculture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Area', models.CharField(max_length=50)),
                ('Productname', models.CharField(max_length=50)),
                ('Quantity', models.IntegerField()),
                ('Status', models.CharField(max_length=50, null=True)),
                ('Agriphoto', models.CharField(max_length=100, null=True)),
                ('Reason', models.CharField(max_length=255, null=True)),
                ('Appno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dces.userreg')),
            ],
        ),
    ]
