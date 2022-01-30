from django.http import JsonResponse,HttpResponse
from django.shortcuts import redirect, render
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from qcm.fonctions import *
#from qcm.forms import UploadFileForm,UploadQuestionForm
from django.contrib.auth.models import User
import time
import os
import random



class StudentShowQuiz(LoginRequiredMixin,View):

	def get(self,request,id_quiz):
		greeting={}
		try:
			name=request.session['username']#le nom de l'utilisateur connecter
			user=User.objects.get(username=name)
			access=user.useraccess
			if str(access.statut) == 'student':
				home_data={}
				home_data['title'] = "Repondre aux questionnaire du quiz {}".format(id_quiz)
				home_data['pageview'] = 'Accuiel'
				return render(request,'student/show_quiz.html',home_data)
			else:
				greeting['error_code'] = '501'
				greeting['error_message']="Utilisateur inconnu!"
				return render(request,'errorpage.html',greeting)

		except Exception as exc:
			greeting['error_code'] = '501'
			greeting['error_message']="Utilisateur inconnu!"
			return render(request,'errorpage.html',greeting)

	def post(self,request):

		if request.method == 'POST':
			greeting={}
			try:
				name=request.session['username']#le nom de l'utilisateur connecter
				user=User.objects.get(username=name)
				access=user.useraccess
				if str(access.statut) == 'student':
					greeting['error_code'] = '501'
					greeting['error_message']="Utilisateur inconnu!"
					return render(request,'errorpage.html',greeting)
				else:
					greeting['error_code'] = '501'
					greeting['error_message']="Utilisateur inconnu!"
					return render(request,'errorpage.html',greeting)
			except Exception as exc:
				greeting['error_code'] = '501'
				greeting['error_message']="Utilisateur inconnu!"
				return render(request,'errorpage.html',greeting)
		else:
			greeting['error_code'] = '501'
			greeting['error_message']="Utilisateur inconnu!"
			return render(request,'errorpage.html',greeting)



class StudentView(LoginRequiredMixin,View):

	def get(self,request):
		greeting={}
		try:
			name=request.session['username']#le nom de l'utilisateur connecter
			user=User.objects.get(username=name)
			access=user.useraccess
			if str(access.statut) == 'student':
				home_data={}
				home_data['title'] = "Repondre aux qcm"
				home_data['pageview'] = 'Accuiel'
				return render(request,'student/index.html',home_data)
			else:
				greeting['error_code'] = '501'
				greeting['error_message']="Utilisateur inconnu!"
				return render(request,'errorpage.html',greeting)

		except Exception as exc:
			greeting['error_code'] = '501'
			greeting['error_message']="Utilisateur inconnu!"
			return render(request,'errorpage.html',greeting)
		




	def post(self,request):
		if request.method == 'POST':
			greeting={}
			try:
				name=request.session['username']#le nom de l'utilisateur connecter
				user=User.objects.get(username=name)
				access=user.useraccess
				if str(access.statut) == 'student':
					greeting['error_code'] = '501'
					greeting['error_message']="Utilisateur inconnu!"
					return render(request,'errorpage.html',greeting)
				else:
					greeting['error_code'] = '501'
					greeting['error_message']="Utilisateur inconnu!"
					return render(request,'errorpage.html',greeting)
			except Exception as exc:
				greeting['error_code'] = '501'
				greeting['error_message']="Utilisateur inconnu!"
				return render(request,'errorpage.html',greeting)

