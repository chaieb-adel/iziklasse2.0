# Generated by Django 3.1.7 on 2022-01-15 21:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auth_group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('manager', 'MANAGER'), ('teacher', 'TEACHER'), ('student', 'STUDENT')], default='student', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BanqueQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('niveau', models.CharField(max_length=200)),
                ('matiere', models.CharField(max_length=200)),
                ('idQuiz', models.IntegerField()),
                ('idUser', models.IntegerField()),
                ('typeQuestion', models.CharField(max_length=200)),
                ('auteur', models.CharField(max_length=200)),
                ('modifications', models.IntegerField()),
                ('datePub', models.DateField(auto_now_add=True)),
                ('question_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Niveau',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('niveau', models.CharField(default='---', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='SimuationQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_quiz', models.IntegerField()),
                ('nombre_question', models.IntegerField()),
                ('cote_par_question', models.CharField(max_length=200)),
                ('maxima', models.IntegerField()),
                ('total_passer', models.IntegerField(default=0)),
                ('total_success', models.IntegerField(default=0)),
                ('total_mised', models.IntegerField(default=0)),
                ('success_indice', models.CharField(default='', max_length=500)),
                ('mised_indice', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Upload_file',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xmlfile', models.FileField(upload_to='xmlquizfiles')),
            ],
        ),
        migrations.CreateModel(
            name='UserAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qcm.auth_group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quizz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('niveau', models.CharField(max_length=100)),
                ('matiere', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('motCles', models.CharField(max_length=200)),
                ('auteur', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('numFichier', models.IntegerField(default=-1)),
                ('quiz_file', models.IntegerField(default=-1)),
                ('xmlfile', models.FileField(default='Aucun fichier', upload_to='xmlquizfiles')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(max_length=100)),
                ('question_text', models.TextField()),
                ('question_image', models.CharField(max_length=250)),
                ('question_name', models.CharField(max_length=250)),
                ('question_externallink', models.CharField(max_length=350)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qcm.quizz')),
            ],
        ),
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cote', models.CharField(max_length=50)),
                ('total_question', models.CharField(max_length=50)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qcm.quizz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Modification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('idBanque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qcm.banquequestion')),
                ('idQuestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qcm.question')),
                ('idUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_fraction', models.CharField(max_length=100)),
                ('answer_text', models.TextField()),
                ('quesion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qcm.question')),
            ],
        ),
    ]
