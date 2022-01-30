from django.http import JsonResponse,HttpResponse
from django.conf import settings
#from qcm.xmlp import CustomQuizzXmlPaerser,save_file
from django.shortcuts import redirect, render
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from qcm.fonctions import *
from qcm.forms import UploadFileForm,AddQuizForm,AttachedFileForm
from django.contrib.auth.models import User
from django.utils import timezone
from qcm.models import SimuationQuiz,BanqueQuestion,Niveau,Matiere,SimuationQuiz,SimQuiz
import time
import os
import random


#adding question manager interface view
class ManagerAddQuestionView(LoginRequiredMixin,View):
	username = [];
	def get(self,request,id_quiz):
		
		try:
			if 'username' in request.session:
				user=User.objects.get(username=request.session['username'])
				access=user.useraccess
				if str(access.statut)== 'manager':
					#utilisateur a acces a cette interface
					quiz=Quizz.objects.get(id=id_quiz)
					has_questions=False
					if len(quiz.question_set.all())>0:
						has_questions=True

					#preparation des donnees pour cette interface
					greeting={}
					greeting['title']="Ajouter une questionaire au quiz {}".format(id_quiz)
					greeting['pageview']="Qcm"
					#greeting['file_q_form']=UploadQuestionForm
					greeting['quiz_id']=id_quiz
					greeting['addform']=AddQuizForm
					greeting['has_questions']=has_questions
					greeting['MEDIA_URL']=settings.MEDIA_URL
					greeting['question_liste']=quiz.question_set.all()
					return render(request,'qcm/manage/add_quiz.html',greeting)
		except Exception as exc:
			print(exc)
			#il s'est passer un truc dans la verification de l'authenticite
			greeting={}
			greeting['error_code'] = '501'
			greeting['error_message']="Attention! vous n'avez pas acces a cette interface! essayer de vous reconnecter!"
			return render(request,'500.html',greeting)

		#l'utilisateur n'a pas access a cette interface
		greeting={}
		greeting['error_code'] = '501'
		greeting['error_message']="Attention! vous n'avez pas acces a cette interface! essayer de vous reconnecter!"
		return render(request,'500.html',greeting)


	def post(self,request,id_quiz):
		data={}
		if (request.method == "POST"):

			#Ajout des questionnaire du quiz
			try:
				if 'username' in request.session:
					name=request.session['username']#le nom de l'utilisateur connecter
					user=User.objects.get(username=name)
					access=user.useraccess
					if str(access.statut) == 'manager':
						if(request.POST.get('add_quiz')):
							data={}
							if save_quiz(request) == 0:
								data["success_message"]=" Quiz ajouter avec success"
								data["id_quiz"]=Quizz.objects.latest('id').id
								return JsonResponse(data, safe=False)
							else:
								data["error_message"]=" Ce quiz pourrais ne pas avoir ete ajouter correctement, veuillez verifier svp!"
							return JsonResponse(data, safe=False)
							#------------//-------------------------------------------------------------

					else:
						data["msg"]=" Vous n'etes pas autoriser a effectuer cet action!"
						return JsonResponse(data, safe=False)

			except Exception as exc:
				print(exc)
				data["msg"]="erreur inconu!!" 
				return JsonResponse(data, safe=False)

			data["msg"]="erreur iinconu!" 
			return JsonResponse(data, safe=False)



#-----------//-----------------------------------------


class ManagerView(LoginRequiredMixin,View):

	def get(self,request):
		greeting={}
		try:
			if 'username' in request.session:
				name=request.session['username']#le nom de l'utilisateur connecter
				user=User.objects.get(username=name)
				access=user.useraccess
				if str(access.statut) == 'manager':
					home_data={}
					home_data['q_liste']=get_all_quiz()
					home_data['title'] = "Banque de questions"
					home_data['pageview'] = 'Qcm'
					home_data['addform']=AddQuizForm
					home_data['filequiz']=AttachedFileForm
					home_data['niveau']=Niveau.objects.all()
					home_data['matiere']=Matiere.objects.all()
					home_data['niveau_liste']=get_all_niveau()
					home_data['matiere_liste']=get_all_matiere()
					home_data['auteur_liste']=get_all_auteur()
					home_data['mot_cles']=get_keywords()

					return render(request,"qcm/manage/index.html",home_data)
				else:
					greeting['error_code'] = '501'
					greeting['error_message']="Utilisateur inconnu!"
					return render(request,'500.html',greeting)
			else:
				greeting['error_code'] = '501'
				greeting['error_message']="Utilisateur inconnu!"
				return render(request,'500.html',greeting)
		except Exception as exc:
			print(exc)
			greeting['error_code'] = '501'
			greeting['error_message']="Utilisateur inconnu!"
			return render(request,'500.html',greeting)


	def post(self,request):
		data={}
		if (request.method == "POST"):
			try:
				if 'username' in request.session:
					name=request.session['username']#le nom de l'utilisateur connecter
					user=User.objects.get(username=name)
					access=user.useraccess
					if str(access.statut) == 'manager':

						#requete d'ajout d'un nouveau quiz a la base de donnees
						if(request.POST.get('add_quiz')):
							data={}
							if save_quiz(request) == 0:
								data["success_message"]=" Quiz ajouter avec success"
								refresh_q_banque()
							else:
								data["error_message"]=" Ce quiz pourrais ne pas avoir ete ajouter correctement, veuillez verifier svp!"
							return JsonResponse(data, safe=False)
						#------------//-------------------------------------------------------------

						#requete ajax quiz par niveau
						elif request.POST.get('s-niveau'):
							data={}
							niveau=request.POST.get('niveau')
							q_liste=filter_by_niveau(niveau)
							data["success_message"]=" Selection quiz du niveau {}".format(niveau)
							data["question_liste"]=q_liste
							return JsonResponse(data, safe=False)
						#---------------//----------------------------------------------------

						#requete ajax quiz par matiere
						elif request.POST.get('s-matiere'):
							data={}
							matiere=request.POST.get('matiere')
							q_liste=filter_by_matiere(matiere)
							data["success_message"]=" Selection quiz matiere {}".format(matiere)
							data["question_liste"]=q_liste
							return JsonResponse(data, safe=False)
						#----------//---------------------------------------------------

						#requete ajax quiz par auteur
						elif request.POST.get('s-auteur'):
							data={}
							auteur=request.POST.get('auteur')
							q_liste=filter_by_auteur(auteur)
							data["success_message"]=" Selection Ajouter par {}".format(auteur)
							data["question_liste"]=q_liste
							return JsonResponse(data, safe=False)
						#----------//-------------------------------------------------------

						#recherches par mots cles
						elif request.POST.get('search'):
							data={}
							try:
								word=request.POST.get('word')
								q_liste=filter_by_word(word)

								if len(q_liste)>=1:
									data["question_liste"]=q_liste
									data["success_message"]=" Résultat de recherche pour {}".format(word)
									return JsonResponse(data, safe=False)
								else:
									data["no_resultat_message"]="Aucun resultat pour votre recherche"
									return JsonResponse(data, safe=False)
							except Exception as exc:
								print(exc)
								data["error_message"]="Aucun resultat pour votre recherche"
								return JsonResponse(data, safe=False)

						#la requete de reception d'un fichier xml de quiz
						else:
							form=UploadFileForm(data=request.POST,files=request.FILES)
							#uploaded_file=request.FILES['file']
							if form.is_valid():
								#saving file to directory media root
								model_instance=form.save(commit=False)
								model_instance.save()
								#---------//-----------------------

								#parsing xml file
								chemin=model_instance.xmlfile #le lien vers le fichier enregistrer en partant du media root
								filePath=os.path.join(settings.MEDIA_ROOT,str(chemin))
								newPath=os.path.join(settings.MEDIA_ROOT,"quiz_xml",str(model_instance.id)+".xml")
								os.rename(filePath,newPath)
								parser=CustomQuizzXmlPaerser(newPath)
								header=parser.get_header()
								header['auteur']=request.session['username']
								nfile=header['nFichier']+int(time.strftime("%s"))
								user=User.objects.get(username=header['auteur'])
								try:
									if model_instance.id > 0:
										file_id=model_instance.id
									else:
										file_id=False
								except Exception as exc:
									file_id=False
								#------------//-----------------------------

								#save quiz to database
								user.quiz_set.create(niveau=header['niveau'],matiere=header['matiere'],description=header['description'],motCles=header['mot_cles'],date=timezone.now(),numFichier=nfile,quiz_file=file_id if file_id != False else -1)
								user.save()
								data["msg"]=" Quiz ajouter avec success"
								return JsonResponse(data, safe=False)
								#----------//--------------------------------

							#form quiz file est invalide
							else:
								data["msg"]=" Desolee ce quiz n'a pas pu etre ajouter verifier si vous avez selectionner un fichier!"
								return JsonResponse(data, safe=False)
							#-----------//----------------------
					else:
						data["msg"]=" Desolee vous n'avez pas l'accees a cette operation! reconnectez vous puis reessayer!"
						return JsonResponse(data, safe=False)
				else:
					data["msg"]=" Votre session de connexion a expirer, actualiser la page!"
					return JsonResponse(data, safe=False)
			except Exception as exc:
				print(exc)
				data['error_code'] = '501'
				data['error_message']="Utilisateur inconnu!"
				return render(request,'500.html',data)



		#la requete n'est ni get ni post
		data["msg"]="request inconu"
		return JsonResponse(data, safe=False)


#delete quiz route
class DeleteQuizView(LoginRequiredMixin,View):

	def get(self,request,id_quiz):
		greeting={}
		try:
			if 'username' in request.session:
				name=request.session['username']#le nom de l'utilisateur connecter
				user=User.objects.get(username=name)
				access=user.useraccess
				if str(access.statut) == 'manager':
					home_data={}
					home_data['q_liste']=get_all_quiz()
					home_data['title'] = "Suppressions quiz {}".format(id_quiz)
					home_data['pageview'] = 'Qcm'
					home_data['quiz_id']=id_quiz
					

					return render(request,"qcm/manage/delete.html",home_data)
				else:
					greeting['error_code'] = '501'
					greeting['error_message']="Utilisateur inconnu!"
					return render(request,'500.html',greeting)
			else:
				greeting['error_code'] = '501'
				greeting['error_message']="Utilisateur inconnu!"
				return render(request,'500.html',greeting)
		except Exception as exc:
			print(exc)
			greeting['error_code'] = '501'
			greeting['error_message']="Utilisateur inconnu!"
			return render(request,'500.html',greeting)
	def post(self,request,id_quiz):
		data={}
		if (request.method == "POST"):
			try:
				if 'username' in request.session:
					name=request.session['username']#le nom de l'utilisateur connecter
					user=User.objects.get(username=name)
					access=user.useraccess
					if str(access.statut) == 'manager':
						if request.POST.get("del_quiz"):
							idi=request.POST.get('id_quiz')
							quiz_=Quizz.objects.get(id=idi)
							if(name == str(quiz_.user)):
								quiz_.delete()
								data['success_message']="Quiz supprimer...Ok!"
								return JsonResponse(data, safe=False)
							else:
								data['success_message']="Ce quiz ne vous appartient pas vous ne pouvez le supprimer! desolee"
								return JsonResponse(data, safe=False)
				else:
					data['error_code'] = '501'
					data['error_message']="Utilisateur inconnu!"
					return render(request,'500.html',greeting)

			except Exception as exc:
				print(exc)
				data['error_message']="Suppression de quiz error"
				return JsonResponse(data, safe=False)


class EditQuizView(LoginRequiredMixin,View):

	def get(self,request,id_quiz):
		greeting={}
		try:
			if 'username' in request.session:
				name=request.session['username']#le nom de l'utilisateur connecter
				user=User.objects.get(username=name)
				access=user.useraccess
				if str(access.statut) == 'manager':
					home_data={}
					home_data['q_liste']=get_all_quiz()
					home_data['title'] = "Modification du quiz {}".format(id_quiz)
					home_data['pageview'] = 'Qcm'
					home_data['quiz_id']=id_quiz
					home_data['addform']=AddQuizForm
					home_data['filequiz']=AttachedFileForm
					home_data['quiz_modif']=Quizz.objects.get(id=id_quiz)
					home_data['niveau']=Niveau.objects.all()
					home_data['matiere']=Matiere.objects.all()
					

					return render(request,"qcm/manage/editquiz.html",home_data)
				else:
					greeting['error_code'] = '501'
					greeting['error_message']="Utilisateur inconnu!"
					return render(request,'500.html',greeting)
			else:
				greeting['error_code'] = '501'
				greeting['error_message']="Utilisateur inconnu!"
				return render(request,'500.html',greeting)
		except Exception as exc:
			print(exc)
			greeting['error_code'] = '501'
			greeting['error_message']="Utilisateur inconnu!"
			return render(request,'500.html',greeting)


	def post(self,request,id_quiz):
		data={}
		if (request.method == "POST"):
			try:
				if 'username' in request.session:
					name=request.session['username']#le nom de l'utilisateur connecter
					user=User.objects.get(username=name)
					access=user.useraccess
					if str(access.statut) == 'manager':
						if request.POST.get("edit_quiz"):
							niveau=request.POST.get('niveau')
							matiere=request.POST.get('matiere')
							description=request.POST.get('description')
							motcles=request.POST.get('motcles')

							quiz=Quizz.objects.get(id=id_quiz)
							quiz.niveau=niveau
							quiz.matiere=matiere
							quiz.description=description
							quiz.motCles=motcles
							quiz.save()
							data['success_message']="Quiz modifié...Ok!"
							return JsonResponse(data, safe=False)
				else:
					data['error_code'] = '501'
					data['error_message']="Utilisateur inconnu!"
					return render(request,'500.html',greeting)

			except Exception as exc:
				print(exc)
				data['error_message']="Suppression de quiz error"
				return JsonResponse(data, safe=False)




class ShowQuizView(LoginRequiredMixin,View):

	def get(self,request,id_quiz):
		greeting={}
		try:
			if 'username' in request.session:
				name=request.session['username']#le nom de l'utilisateur connecter
				user=User.objects.get(username=name)
				access=user.useraccess
				if str(access.statut) == 'manager':
					home_data={}
					quiz=Quizz.objects.get(id=id_quiz)
					if len(quiz.question_set.all())>0:
						has_questions=True
						length=len(quiz.question_set.all())
					if len(SimuationQuiz.objects.all())>0:
						#on efface tout
						SimuationQuiz.objects.all().delete()
					home_data['title'] = "Visualisation en mode eleve, quiz {}".format(id_quiz)
					home_data['pageview'] = 'Qcm'
					home_data['quiz_id']=id_quiz
					home_data['nbr_q']=len(quiz.question_set.all())
					home_data['cotes']=float(str(20/home_data['nbr_q']).split(".")[0] +"."+str(20/home_data['nbr_q']).split(".")[1][:2])
					home_data['maxima']=20
					home_data['cote']=float(str(home_data['maxima']/home_data['nbr_q']).split(".")[0] +"."+str(home_data['maxima']/home_data['nbr_q']).split(".")[1][:2])
					new_simu=SimuationQuiz(id_quiz=id_quiz, nombre_question=length,cote_par_question=str(home_data['cote']), maxima=home_data['maxima'])
					new_simu.save()
					return render(request,"qcm/manage/show_quiz.html",home_data)
				else:
					greeting['error_code'] = '501'
					greeting['error_message']="Utilisateur inconnu!"
					return render(request,'500.html',greeting)
			else:
				greeting['error_code'] = '501'
				greeting['error_message']="Utilisateur inconnu!"
				return render(request,'500.html',greeting)
		except Exception as exc:
			print(exc)
			greeting['error_code'] = '501'
			greeting['error_message']="Utilisateur inconnu!"
			return render(request,'500.html',greeting)

class ReUseView(LoginRequiredMixin,View):

	def get(self,request,id_quiz):
		try:
			if 'username' in request.session:
				user=User.objects.get(username=request.session['username'])
				access=user.useraccess
				if str(access.statut)== 'manager':
					#utilisateur a acces a cette interface
					quiz=Quizz.objects.get(id=id_quiz)
					has_questions=False
					if len(quiz.question_set.all())>0:
						has_questions=True

					#preparation des donnees pour cette interface
					greeting={}
					greeting['title']="Reutilisation du quiz {}".format(id_quiz)
					greeting['pageview']="Qcm"
					#greeting['file_q_form']=UploadQuestionForm
					greeting['quiz_id']=id_quiz
					greeting['addform']=AddQuizForm
					greeting['has_questions']=has_questions
					greeting['question_liste']=quiz.question_set.all()
					return render(request,'qcm/manage/reusemodel.html',greeting)
		except Exception as exc:
			print(exc)
			#il s'est passer un truc dans la verification de l'authenticite
			greeting={}
			greeting['error_code'] = '501'
			greeting['error_message']="Attention! vous n'avez pas acces a cette interface! essayer de vous reconnecter!"
			return render(request,'500.html',greeting)

		#l'utilisateur n'a pas access a cette interface
		greeting={}
		greeting['error_code'] = '501'
		greeting['error_message']="Attention! vous n'avez pas acces a cette interface! essayer de vous reconnecter!"
		return render(request,'500.html',greeting)


	def post(self,request,id_quiz):
		data={}
		if (request.method == "POST"):
			try:
				if 'username' in request.session:
					name=request.session['username']#le nom de l'utilisateur connecter
					user=User.objects.get(username=name)
					access=user.useraccess
					if str(access.statut) == 'manager':
						if request.POST.get("reuse_quiz"):
							niveau=request.POST.get('niveau')
							matiere=request.POST.get('matiere')
							description=request.POST.get('description')
							motcles=request.POST.get('motcles')
							questionnaire=request.POST.get("questionnaire").split(",")
							old_quiz=request.POST.get("old_quiz")

							quiz=Quizz(user=user, niveau=niveau, matiere=matiere, description=description,motCles=motcles,auteur=str(user), date=timezone.now())
							quiz.save()
							for q in list(questionnaire):
								question=Question.objects.get(id=int(q))
								quiz.question_set.create(question_type=question.question_type,question_text=question.question_text,question_image=question.question_image,question_name=question.question_name,question_externallink=question.question_externallink)

							quiz.save()
							data['success_message']="Quiz enregistré...Ok!"
							data['quiz_id']=quiz.id
							return JsonResponse(data, safe=False)
				else:
					data['error_code'] = '501'
					data['error_message']="Utilisateur inconnu!"
					return render(request,'500.html',greeting)

			except Exception as exc:
				print(exc)
				data['error_message']="Suppression de quiz error"
				return JsonResponse(data, safe=False)


#------A quoi Sert il ?--------------------------
class DoQuizView(LoginRequiredMixin,View):
	question_liste=[]
	def get(self,request,id_quiz):
		
		try:
			if 'username' in request.session:
				user=User.objects.get(username=request.session['username'])
				access=user.useraccess
				if str(access.statut)== 'manager':
					#utilisateur a acces a cette interface
					quiz=Quizz.objects.get(id=id_quiz)
					has_questions=False
					if len(quiz.question_set.all())>0:
						has_questions=True
						length=len(quiz.question_set.all())


					#preparation des donnees pour cette interface
					greeting={}
					greeting['title']="Repondez au questionnaire du quiz {}".format(id_quiz)
					greeting['pageview']="Acceuil"
					greeting["nbr_q"] = length
					#greeting['file_q_form']=UploadQuestionForm
					question_liste=quiz.question_set.all()
					greeting['quiz_id']=id_quiz
					greeting['first_q']=question_liste[0]
					greeting['numero_q']=1
					greeting['maxima']=20
					greeting['cote']=float(str(greeting['maxima']/greeting['nbr_q']).split(".")[0] +"."+str(greeting['maxima']/greeting['nbr_q']).split(".")[1][:2])
					greeting['reponses']=greeting['first_q'].answer_set.all()
					#home_data['title'] = "Visualisation en mode eleve, quiz {}".format(id_quiz)
					#home_data['pageview'] = 'Qcm'
					#home_data['quiz_id']=id_quiz
					greeting['nbr_q']=len(quiz.question_set.all())
					#home_data['cotes']=float(str(20/home_data['nbr_q']).split(".")[0] +"."+str(20/home_data['nbr_q']).split(".")[1][:2])
					
					#greeting['addform']=AddQuizForm
					#greeting['has_questions']=has_questions
					greeting['question_liste']=quiz.question_set.all()
					return render(request,'qcm/manage/doquiz.html',greeting)
					#return HttpResponse(indice_question)
		except Exception as exc:
			print(exc)
			#il s'est passer un truc dans la verification de l'authenticite
			greeting={}
			greeting['error_code'] = '501'
			greeting['error_message']="Attention! vous n'avez pas acces a cette interface! essayer de vous reconnecter!"
			return render(request,'500.html',greeting)

		#l'utilisateur n'a pas access a cette interface
		greeting={}
		greeting['error_code'] = '501'
		greeting['error_message']="Attention! vous n'avez pas acces a cette interface! essayer de vous reconnecter!"
		return render(request,'500.html',greeting)


	def post(self,request,id_quiz):
		data={}
		question_liste=[]
		if (request.method == "POST"):
			try:
				if 'username' in request.session:
					name=request.session['username']#le nom de l'utilisateur connecter
					user=User.objects.get(username=name)
					access=user.useraccess
					if str(access.statut) == 'manager':
						quiz=Quizz.objects.get(id=id_quiz)
						question_liste=quiz.question_set.all()
						if request.POST.get("driven_quiz"):
							current_q=request.POST.get('current_q')
							action=request.POST.get('action')
							current_q=int(current_q)+1
							try:
								quest=question_liste[current_q]
								data['q_numero']=current_q
								data['nbr_q']=len(question_liste)
								data['q_name']=quest.question_name
								data['cote']=float(str(20/data['nbr_q']).split(".")[0] +"."+str(20/data['nbr_q']).split(".")[1][:2])
								data['q_type']=quest.question_type
								
								#question complexe
								if "{:" in quest.question_text:
									data['q_text']=reponsecutter(quest.question_text)['question']
									data['short_answer']=reponsecutter(quest.question_text)['short_answer']
								else:
									data['q_text']=quest.question_text
									data['short_answer']=reponsecutter(quest.question_text)['short_answer']
								data['q_image']=quest.question_image
								data['true_libre']=False
								data['trou_liste']=True if True in ("unique", "liste" in data['q_name']) else False
								data['true_liste']=False
								data['choix_unique']=True
								data['q_external']=quest.question_externallink
								data['reponses']=[]
								print("Next question....{}".format(current_q))
							
								for a in quest.answer_set.all():
									rep={
									'fraction':a.answer_fraction,
									"text":a.answer_text
									}
									data['reponses'].append(rep)

								data['success_message']="Question suivante..."
								data['quiz_id']=id_quiz
								print(data['q_type'])
								return JsonResponse(data, safe=False)
							except Exception as exc:
								print(exc)
								data['nbr_q']=len(question_liste)
								data['q_numero']=data['nbr_q']
								data['success_message']="Vous avez fini le quiz bravo"
								data['quiz_id']=id_quiz
								data['no-question']="plus de question..."
								return JsonResponse(data, safe=False)
				else:
					data['error_code'] = '501'
					data['error_message']="Utilisateur inconnu!"
					return render(request,'500.html',greeting)

			except Exception as exc:
				print(exc)
				data['error_message']="Suppression de quiz error"
				return JsonResponse(data, safe=False)
#-----------------------------------//--------------------------------------------

class DelQuestView(LoginRequiredMixin,View):
	question_liste=[]
	def get(self,request,id_question):
		
		try:
			if 'username' in request.session:
				data={}
				user=User.objects.get(username=request.session['username'])
				access=user.useraccess
				if str(access.statut)== 'manager':
					#utilisateur a acces a cette interface
					try:
						question=Question.objects.get(id=id_question)
						quiz=Quizz.objects.get(id=question.quiz.id)
						data['question_indice']=question.id
						data['quiz_id']=quiz.id
						data['niveau']=quiz.niveau
						data['matiere']=quiz.matiere
						data['date_pub']=quiz.date
						#suppression de la qustion
						question.delete()
						data['nbr_question']=len(quiz.question_set.all())
						return render(request,'qcm/manage/delquestion.html',data)
					except Exception as exc:
						return redirect("dashboard")

					

		except Exception as exc:
			print(exc)
			data={}
			data['error_code'] = '501'
			data['error_message']="Utilisateur inconnu!"
			return render(request,'500.html',data)




class ShowQuestionView(LoginRequiredMixin,View):
	question_liste=[]
	def get(self,request,indice_question):
		"""Retourne une question suivant l'indice"""
		data={}
		try:
			if 'username' in request.session:
				user=User.objects.get(username=request.session['username'])
				access=user.useraccess
				if str(access.statut)== 'manager':
					#utilisateur a acces a cette interface
					simulation=SimuationQuiz.objects.all()
					simulation=simulation[0]
					cote_per=simulation.cote_par_question
					quiz=Quizz.objects.get(id=simulation.id_quiz)
					question_liste=quiz.question_set.all()
					data['next_q']=indice_question
					data['cote']=cote_per
					data['MEDIA_URL']=settings.MEDIA_URL
					data['question_name']=''
					data['question_titre']=''
					data['question_type']=''
					data['question_image']=''
					data['question_link']=''
					if indice_question == 0:
						data['start_quiz']=True
					else:
						data['start_quiz']=False

					data['total_question']=question_liste
					data['nombre_of']=len(data['total_question'])
					data['current']=1
					data['rep_indice']=0
					if indice_question == 1:
						siml=SimQuiz.objects.get(id=1)
						siml.missed="---"
						siml.success="---"
						siml.save()
						next_q=question_liste[indice_question-1]
						data['next_q']=indice_question+1
						data['question_name']=next_q.question_name
						data['question_type']=next_q.question_type

						#Question a choix multiple avec des balises answer
						if next_q.question_type == 'multichoice':
							reponses=next_q.answer_set.all()
							data['reponses']=reponses
							data['question_titre']=next_q.question_text
							data['question_image']=next_q.question_image
							data['question_link']=next_q.question_externallink
							if "choix unique" in next_q.question_name:
								data['choix_unique']=True
							elif "choix multiple" in next_q.question_name:
								data['choix_multiple']=True

						#Des reponse dans la question
						elif next_q.question_type == 'cloze':
							#le question contient des indice pour la position de ses reponse dans la table de reponse
							#le short answer n'en contient que une
							#on parcours les bribes , indice de la bribe est l'indice de sa ou ses reponse
							data_resultat=reponsecutter(next_q.question_text)
							data['answer_liste']=data_resultat['reponse']
							if data_resultat['short_answer']:
								data['short_answer']=True
								rep_liste=[]
								for r in data['answer_liste']:
									r=r.split("%")[2]
									rep_liste.append(r)
								data['answer_liste']=rep_liste
							else:
								rep_=[]#liste contenant des liste de reponse pour chaque bribe
								for r in data['answer_liste']:#[%100%tetete~%0%tetdgdt]
									rrr=r.split("~")#[%100%textgdg,%0%tetxxggss,.....]
									r_clean=[]#les reps pour la bribe actuel
									#r_clean=[{'fraction':100, 'text':'text'}]
									for r in rrr:
										if r:
											repo=r.split("%")
											reee={
											'fraction':repo[1],
											'text':repo[2]
											}
											r_clean.append(reee)
									rep_.append(r_clean)
								data['answer_liste']=rep_


									
								
							data['question']=data_resultat['question'].split(";")
							#print(data['answer_liste'])
							if True in ("trous","libre" in next_q.question_name):
								#complexe avec des saisi
								data['trous_libre']=True
							elif True in ("trous","liste" in next_q.question_name):
								#complexe avec selection
								data['trous_liste']=True
						elif next_q.question_type == 'shortanswer':
							data['shortanswer']=True
							data['question_titre']=next_q.question_text
							reponses=next_q.answer_set.all()
							data['reponses']=reponses
						elif next_q.question_type == 'numerical':
							data['shortanswer']=True
							data['question_titre']=next_q.question_text
							reponses=next_q.answer_set.all()
							data['reponses']=reponses
						elif next_q.question_type == 'spellanswer':
							data['shortanswer']=True
							data['question_titre']=next_q.question_text
							reponses=next_q.answer_set.all()
							data['reponses']=reponses
						elif "{:SHORTANSWER" in next_q.question_text:
							data_resultat=reponsecutter(next_q.question_text)
							data['answer_liste']=data_resultat['reponse']
							if data_resultat['short_answer']:
								data['short_answer']=True
								rep_liste=[]
								for r in data['answer_liste']:
									r=r.split("%")[2]
									rep_liste.append(r)
								data['answer_liste']=rep_liste
						elif "{:MULTICHOICE" in next_q.question_text:
							rep_=[]#liste contenant des liste de reponse pour chaque bribe
							for r in data['answer_liste']:#[%100%tetete~%0%tetdgdt]
								rrr=r.split("~")#[%100%textgdg,%0%tetxxggss,.....]
								r_clean=[]#les reps pour la bribe actuel
								#r_clean=[{'fraction':100, 'text':'text'}]
								for r in rrr:
									if r:
										repo=r.split("%")
										reee={
										'fraction':repo[1],
										'text':repo[2]
										}
										r_clean.append(reee)
								rep_.append(r_clean)
							data['answer_liste']=rep_
						elif next_q.question_type == 'matching':
							data['matching']=True
							data['question_titre']=next_q.question_text
							reponses=next_q.answer_set.all()
							data['reponses']=reponses


					elif indice_question >1:
						#si nous somme a la fin
						if indice_question<= len(question_liste):
							next_q=question_liste[indice_question-1]
							data['next_q']=indice_question+1
							data['question_name']=next_q.question_name
							data['current']=indice_question
							data['question_type']=next_q.question_type

							#Question a choix multiple avec des balises answer
							if next_q.question_type == 'multichoice':
								reponses=next_q.answer_set.all()
								data['reponses']=reponses
								data['question_titre']=next_q.question_text
								data['question_image']=next_q.question_image
								data['question_link']=next_q.question_externallink
								if "choix unique" in next_q.question_name:
									data['choix_unique']=True
								elif "choix multiple" in next_q.question_name:
									data['choix_multiple']=True

							#Des reponse dans la question
							elif next_q.question_type == 'cloze':
								#le question contient des indice pour la position de ses reponse dans la table de reponse
								#le short answer n'en contient que une
								#on parcours les bribes , indice de la bribe est l'indice de sa ou ses reponse
								data_resultat=reponsecutter(next_q.question_text)
								data['answer_liste']=data_resultat['reponse']
								if data_resultat['short_answer']:
									data['short_answer']=True
									rep_liste=[]
									for r in data['answer_liste']:
										r=r.split("%")[2]
										rep_liste.append(r)
									data['answer_liste']=rep_liste
								else:
									rep_=[]#liste contenant des liste de reponse pour chaque bribe
									for r in data['answer_liste']:#[%100%tetete~%0%tetdgdt]
										rrr=r.split("~")#[%100%textgdg,%0%tetxxggss,.....]
										r_clean=[]#les reps pour la bribe actuel
										#r_clean=[{'fraction':100, 'text':'text'}]
										for r in rrr:
											if r:
												repo=r.split("%")
												reee={
												'fraction':repo[1],
												'text':repo[2]
												}
												r_clean.append(reee)
										rep_.append(r_clean)
									data['answer_liste']=rep_


									
								
								data['question']=data_resultat['question'].split(";")
								#print(data['answer_liste'])
								if True in ("trous","libre" in next_q.question_name):
									#complexe avec des saisi
									data['trous_libre']=True
								elif True in ("trous","liste" in next_q.question_name):
									#complexe avec selection
									data['trous_liste']=True
							elif next_q.question_type == 'shortanswer':
								data['shortanswer']=True
								data['question_titre']=next_q.question_text
								reponses=next_q.answer_set.all()
								data['reponses']=reponses
							elif next_q.question_type == 'numerical':
								data['shortanswer']=True
								data['question_titre']=next_q.question_text
								reponses=next_q.answer_set.all()
								data['reponses']=reponses
							elif next_q.question_type == 'spellanswer':
								data['shortanswer']=True
								data['question_titre']=next_q.question_text
								reponses=next_q.answer_set.all()
								data['reponses']=reponses
							elif "{:SHORTANSWER" in next_q.question_text:
								data_resultat=reponsecutter(next_q.question_text)
								data['answer_liste']=data_resultat['reponse']
								if data_resultat['short_answer']:
									data['short_answer']=True
									rep_liste=[]
									for r in data['answer_liste']:
										r=r.split("%")[2]
										rep_liste.append(r)
									data['answer_liste']=rep_liste
							elif "{:MULTICHOICE" in next_q.question_text:
								rep_=[]#liste contenant des liste de reponse pour chaque bribe
								for r in data['answer_liste']:#[%100%tetete~%0%tetdgdt]
									rrr=r.split("~")#[%100%textgdg,%0%tetxxggss,.....]
									r_clean=[]#les reps pour la bribe actuel
									#r_clean=[{'fraction':100, 'text':'text'}]
									for r in rrr:
										if r:
											repo=r.split("%")
											reee={
											'fraction':repo[1],
											'text':repo[2]
											}
											r_clean.append(reee)
									rep_.append(r_clean)
								data['answer_liste']=rep_
							elif next_q.question_type == 'matching':
								data['matching']=True
								data['question_titre']=next_q.question_text
								reponses=next_q.answer_set.all()
								data['reponses']=reponses

						else:
							data['end_quiz']=True
					stau=SimQuiz.objects.get(id=1)
					missed=stau.missed
					success=stau.success
					data['missed_liste']=getMissedIndece(missed)
					data['missed_length']=len(data['missed_liste'])
					data['success_liste']=getSuccessIndece(success)
					data['success_length']=len(data['success_liste'])
					data['missed_percent']=round((data['missed_length']/data['nombre_of'])*100)
					data['success_percent']=round((data['success_length']/data['nombre_of'])*100)
					data['title']="Repondez au questionnaire du quiz {}".format(simulation.id_quiz)
					data['pageview']="Acceuil"
					return render(request, 'qcm/manage/doquiz.html', data)
		except Exception as exc:
			print(exc)
			data['error_code'] = '501'
			data['error_message']="Utilisateur inconnu!"
			return render(request,'500.html',data)
	def post(self,request,indice_question):
		data={}
		if (request.method == "POST"):
			#enregistrer les question patthern de reussite et d'achec
			try:
				if 'username' in request.session:
					if(request.POST.get('missed')):
						current=request.POST.get('current')
						
						c=SimQuiz.objects.get(id=1)
						if str(current) not in c.missed:
							c.missed=c.missed+"-"+current
							c.save()
							data["success_message"]=" Quiz ajouter avec success"
						else:
							data["success_message"]="deja dans echouer!!"
						return JsonResponse(data, safe=False)
					elif(request.POST.get('success')):
						current=request.POST.get('current')
						
						c=SimQuiz.objects.get(id=1)
						if str(current) not in c.success:
							c.success=c.success+current+"-"
							c.save()
							data["success_message"]=" Quiz ajouter avec success"
						else:
							data["success_message"]="deja dans echouer!!"
						return JsonResponse(data, safe=False)
			except Exception as exc:
				print(exc)
				data["success_message"]=" Quiz ajouter avec success"
				return JsonResponse(data, safe=False)
					



