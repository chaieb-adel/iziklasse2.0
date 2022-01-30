from django.http import request
#from django.urls import reverse
from django.shortcuts import redirect, render
from django.http import JsonResponse,HttpResponse
from django.views import View   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from qcm.xmlp import CustomQuizzXmlPaerser,save_file
from .forms import UploadFileForm,UploadQuestionForm
from django.utils import timezone
from django.conf import settings
#from authentication import views
from authentication.forms import UserLoginForm
import time
import os
import random
from qcm.fonctions import *

class AddQuestionView(LoginRequiredMixin,View):
    username = [];
    def get(self,request,id_quiz):
        #print(id_quiz)
        if 'username' in request.session:
            user=User.objects.get(username=request.session['username'])
            access=user.useraccess
            if str(access.statut)== 'manager':
                #return redirect('dashboard')
                #getting quiz
                quiz=Quiz.objects.get(id=id_quiz)
                has_questions=False
                if len(quiz.question_set.all())>0:
                    has_questions=True

                greeting={}
                greeting['title']="Ajouter une questionaire au quiz {}".format(id_quiz)
                greeting['pageview']="Qcm"
                greeting['file_q_form']=UploadQuestionForm
                greeting['quiz_id']=id_quiz
                #has_questions=False
                greeting['has_questions']=has_questions
                greeting['question_liste']=quiz.question_set.all()
                return render(request,'manage/add_quiz.html',greeting)

        greeting={}
        greeting['form'] = UserLoginForm
        return render(request,'pages/authentication/auth-login.html',greeting)
            


    def post(self,request,id_quiz):
        data={}
        if (request.method == "POST"):
            #Adding quiz request from xml and from formulaire
            if 'username' in request.session:

                form=UploadQuestionForm(data=request.POST,files=request.FILES)
                #uploaded_file=request.FILES['file']
                if form.is_valid():
                    model_instance=form.save(commit=False)
                    #model_instance.name="quiz-{}{}".format(random.randrange(278826726277887),".xml")
                    model_instance.save()

                    chemin=model_instance.xmlfile #le lien vers le fichier enregistrer en partant du media root
                    filePath=os.path.join(settings.MEDIA_ROOT,str(chemin))
                    newPath=os.path.join(settings.MEDIA_ROOT,"quiz_question",str(model_instance.id)+".xml")
                    os.rename(filePath,newPath)
                    parser=CustomQuizzXmlPaerser(newPath)
                    questions_liste=parser.get_multichoice_q_liste()
                    quiz=Quiz.objects.get(id=id_quiz)
                    for question in questions_liste:
                        save_question(question,quiz)


                    """header['auteur']=request.session['username']
                    nfile=header['nFichier']+int(time.strftime("%s"))
                    user=User.objects.get(username=header['auteur'])

                    try:
                        if model_instance.id > 0:
                            file_id=model_instance.id
                        else:
                            file_id=False
                    except Exception as exc:
                        file_id=False
                    user.quiz_set.create(niveau=header['niveau'],matiere=header['matiere'],description=header['description'],motCles=header['mot_cles'],date=timezone.now(),numFichier=nfile,quiz_file=file_id if file_id != False else -1)
                    user.save()"""
                    data["msg"]=" Quiz ajouter avec success"

                    return JsonResponse(data, safe=False)

                else:
                    data["msg"]=" Desolee ce quiz n'a pas pu etre ajouter!"
                    
                    return JsonResponse(data, safe=False)
            data["msg"]="request inconu" 
            return JsonResponse(data, safe=False)