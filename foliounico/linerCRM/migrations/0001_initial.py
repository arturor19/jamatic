# Generated by Django 5.0.2 on 2024-08-04 02:30

import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=255)),
                ('direccion', models.TextField()),
                ('telefono', models.CharField(blank=True, max_length=10, null=True)),
                ('direccion_mac', models.CharField(blank=True, max_length=17, null=True)),
                ('red', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_alta', models.DateField(default=django.utils.timezone.now)),
                ('cuota', models.DecimalField(decimal_places=2, default=200.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('fecha_de_alta', models.DateField(blank=True, null=True)),
                ('nombre_completo', models.CharField(blank=True, max_length=255)),
                ('rol', models.CharField(choices=[('Agente Nacional', 'Agente Nacional'), ('Agente Internacional', 'Agente Internacional'), ('Cerrador Nacional', 'Cerrador Nacional'), ('Cerrador Internacional', 'Cerrador Internacional'), ('Secretaria', 'Secretaria'), ('Superadmin', 'Superadmin')], default='Secretaria', max_length=30)),
                ('is_staff', models.BooleanField(default=True, help_text='Designa si el usuario puede iniciar sesión en el sitio de administración.', verbose_name='staff status')),
                ('numero_telefono', models.CharField(max_length=10, verbose_name='Número de teléfono')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pago', models.DateField(default=django.utils.timezone.now)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('recibo', models.CharField(blank=True, max_length=255, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagos', to='linerCRM.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='ReporteFalla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('fecha_reporte', models.DateTimeField(auto_now_add=True)),
                ('solucionado', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportes', to='linerCRM.cliente')),
            ],
            options={
                'verbose_name_plural': 'Reportes de Fallas',
            },
        ),
    ]
