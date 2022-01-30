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





class TeacherView(LoginRequiredMixin,View):

	def get(self,request):
		greeting={}
		try:
			if 'username' in request.session:
				user=User.objects.get(username=request.session['username'])
				access=user.useraccess
				if str(access.statut)== 'teacher':
					home_data={}
					home_data['q_liste']=[]#get_users_quiz(user)
					home_data['title'] = "mes quizs"
					home_data['pageview'] = 'Qcm'

					return render(request,'teacher/index.html',home_data)

			greeting['error_code'] = '501'
			greeting['error_message']="Attention! vous n'avez pas acces a cette interface! essayer de vous reconnecter!"
			return render(request,'errorpage.html',greeting)

		except Exception as exc:
			print(exc)
			greeting['error_code'] = '501'
			greeting['error_message']="Attention! vous n'avez pas acces a cette interface! essayer de vous reconnecter!"
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
