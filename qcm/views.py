""""
    
    IZIEVAL routes liste and ajax endpoint!

"""
from django.http import request
from django.urls import reverse
from django.shortcuts import redirect, render
from django.http import JsonResponse,HttpResponse
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
#from qcm.xmlp import save_file
#from .forms import UploadFileForm,UploadQuestionForm
from django.utils import timezone
from django.conf import settings
#from authentication import views
from authentication.forms import UserLoginForm
import time
import os
import random
from qcm.fonctions import *
#from qcm.addquestionview import *

#manage route
from qcm.manage.managerview import *
#teaher route
from qcm.teacher.teacherview import *
#student route
from qcm.student.studentview import *


#home route view
class DashboardView(LoginRequiredMixin,View):

    def get(self, request):
        greeting={}
        try:
            name=request.session['username']#le nom de l'utilisateur connecter
            user=User.objects.get(username=name)
            access=user.useraccess

        except Exception as exc:
            print(exc)
            greeting['error_code'] = '501'
            greeting['error_message']="Utilisateur inconnu!"
            return render(request,'500.html',greeting)
        if str(access.statut) == 'manager':
            #l'utisateur est un gere la banque de donnees
            return redirect('manager')

        elif str(access.statut) == 'teacher':
            #l'utilisateur est un professeur
            return redirect('teacher')


        elif str(access.statut) == 'student':
            
            return redirect('student')

        #l'utilisateur n'a pas d'access manager
       
        
        greeting={}
        greeting['error_code'] = '501'
        greeting['error_message']="Access a l'application interdit!"
        return render(request,'500.html',greeting)
       
            

    



    def post(self,request):

        pass

