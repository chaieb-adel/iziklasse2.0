from django.db import models
from django.contrib.auth.models import User
import datetime
from django.http import request
# Create your models here.


GROUP_CHOICE=(
	('manager','MANAGER'),
	('teacher','TEACHER'),
	('student','STUDENT')
	)

class Niveau(models.Model):
	niveau=models.CharField(max_length=150,default="---")

	def __str__(self):
		return self.niveau

class Matiere(models.Model):
	matiere=models.CharField(max_length=150,default="---")

	def __str__(self):
		return self.matiere


class Auth_group(models.Model):

	name=models.CharField(max_length=100, choices=GROUP_CHOICE,default='student')
	

	def __str__(self):
		return self.name


class UserAccess(models.Model):

	user=models.OneToOneField(User, on_delete=models.CASCADE)
	statut=models.ForeignKey(Auth_group,on_delete=models.CASCADE)


	def __str__(self):
		return "{}:{}".format(self.user,self.statut)



#niveau=forms.ChoiceField(choices=CHOICES_NIVEAU)
class Quizz(models.Model):

	user=models.ForeignKey(User,on_delete=models.CASCADE)
	niveau=models.TextField()
	matiere=models.TextField()
	description=models.TextField()
	motCles=models.CharField(max_length=200)
	auteur=models.CharField(max_length=200)
	date=models.DateTimeField(auto_now_add=True)
	numFichier=models.IntegerField(default=-1)
	quiz_file=models.IntegerField(default=-1)
	xmlfile=models.FileField(upload_to="xmlquizfiles",default="Aucun fichier")

	def __str__(self):
		return self.matiere

class SimuationQuiz(models.Model):
	id_quiz=models.IntegerField()
	nombre_question=models.IntegerField()
	cote_par_question=models.CharField(max_length=200)
	maxima=models.IntegerField()
	total_passer=models.IntegerField(default=0)
	total_success=models.IntegerField(default=0)
	total_mised=models.IntegerField(default=0)
	success_indice=models.CharField(max_length=500, default='')#eg:"1,2,4,5,6,8"
	mised_indice=models.CharField(max_length=500, default='')

class SimQuiz(models.Model):
	missed=models.TextField()
	success=models.TextField()

#apres l'enregistrement du fichier le quiz est creer et peu donc prendre l'id du fichier si pertinance est
class Upload_file(models.Model):
	"""Ajout d'un fichier de quiz"""
	xmlfile=models.FileField(upload_to="xmlquizfiles")


"""class Upload_question(models.Model):
	
	xmlfile=models.FileField(upload_to="quiz_question")"""
"""class Images_q_base(models.Model):

	image=models.FileField(upload_to="images",default="Aucun fichier")
	question=models.ForeignKey(Question, on_delete=models.CASCADE)"""

class Question(models.Model):

	quiz=models.ForeignKey(Quizz, on_delete=models.CASCADE)
	question_type=models.CharField(max_length=100)
	question_text=models.TextField()
	question_image=models.CharField(max_length=250)
	question_name=models.CharField(max_length=250)
	question_externallink=models.CharField(max_length=350)


	def __str__(self):

		return self.question_text


class Answer(models.Model):

	quesion=models.ForeignKey(Question, on_delete=models.CASCADE)
	answer_fraction=models.CharField(max_length=100)
	answer_text=models.TextField()

	def __str__(self):

		return self.answer_text


class Points(models.Model):

	quiz=models.ForeignKey(Quizz, on_delete=models.CASCADE)
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	cote=models.CharField(max_length=50)
	total_question=models.CharField(max_length=50)


	def __str__(self):
		return self.cote

class BanqueQuestion(models.Model):


	niveau=models.CharField(max_length=200)
	matiere=models.CharField(max_length=200)
	idQuiz=models.IntegerField()
	idUser=models.IntegerField()
	typeQuestion=models.CharField(max_length=200)
	auteur=models.CharField(max_length=200)
	modifications=models.IntegerField()
	datePub=models.DateField(auto_now_add=True)
	question_text=models.TextField()


	def __str__(self):

		return self.question_text

class BqAnswer(models.Model):

	quesion=models.ForeignKey(BanqueQuestion, on_delete=models.CASCADE)
	answer_fraction=models.CharField(max_length=100)
	answer_text=models.TextField()

	def __str__(self):

		return self.answer_text


class Modification(models.Model):

	idBanque=models.ForeignKey(BanqueQuestion, on_delete=models.CASCADE)#l'ancienne version de la question
	idUser=models.ForeignKey(User, on_delete=models.CASCADE)
	date=models.DateField(auto_now_add=True)
	idQuestion=models.ForeignKey(Question, on_delete=models.CASCADE)#apres enregistrement la questio est vu comme nouvelle depuis la table question




class Getdata():

	def __init__(self, model):
		self.model=model

	def get_all(self):
		data=models.objects.all()

	def get_child_relation(self,db_entry):
		pass



