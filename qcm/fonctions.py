from .models import Auth_group,Quizz,Question,Upload_file,Answer,BanqueQuestion
from qcm.forms import UploadFileForm,AddQuizForm,AttachedFileForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from qcm.xmlp import ParseXml
import re

import os




def getSuccessIndece(text_pattern):
    """Extraire la liste des quiz deja resusi"""
    if(text_pattern == "---"):
        return []
    clean_up1=text_pattern.replace("---","")
    to_list=clean_up1.split("-")
    clean_up2=[]
    #remove blank
    for string in to_list:
        if string != "":
            clean_up2.append(string)
    #convert to string
    if(len(clean_up2)>0):
        clean_up2=[int(n) for n in clean_up2]
    if(len(clean_up2)>0):
        return clean_up2
    else:
        return []

def getMissedIndece(text_pattern):
    """Extraire la liste des quiz deja resusi"""
    if(text_pattern == "---"):
        return []
    clean_up1=text_pattern.replace("---","")
    to_list=clean_up1.split("-")
    clean_up2=[]
    #remove blank
    for string in to_list:
        if string != "":
            clean_up2.append(string)
    #convert to string
    if(len(clean_up2)>0):
        clean_up2=[int(n) for n in clean_up2]
    if(len(clean_up2)>0):
        return clean_up2
    else:
        return []



def cloze_question(next_q):
    data={}
    data_resultat=reponsecutter(next_q.question_text)
    data['answer_liste']=data_resultat['reponse']
    if data_resultat['short_answer']:
        data['short_answer']=True
        rep_liste=[]
        for r in data['answer_liste']:
            r=r.split("%")[2]
            rep_liste.append(r)
            data['answer_liste']=rep_liste
        return data
    else:
        rep_=[]#liste contenant des liste de reponse pour chaque bribe
        for r in data['answer_liste']:#[%100%tetete~%0%tetdgdt]
            rrr=r.split("~")#[%100%textgdg,%0%tetxxggss,.....]
            r_clean=[]#les reps pour la bribe actuel
            #r_clean=[{'fraction':100, 'text':'text'}]
            for r in rrr:
                if r:
                    repo=r.split("%")
                    eee={
                        'fraction':repo[1],
                        'text':repo[2]
                        }
                    r_clean.append(reee)
                rep_.append(r_clean)
                data['answer_liste']=rep_
        return data
quiz_id_cache=0
def regex_manager(strr):
    regex=r'[a-zA-Z]* {:[A-Za-z]*:%[0-9]*%[a-zA-Z]*#~%[0-9]*%[a-zA-Z]*#~%[0-9]*%[a-zA-Z0-9]*#~%[0-9]*%[a-zA-Z0-9]*#}'
    regex2=r'[A-Za-z ]*[ {]'
    question=''
    matches=re.finditer(regex2, strr)
    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
        question+=match.group()
    question=question.replace("{","---")
    return question

def reponsecutter(text):
    """Extrait les reponse dans une question complexe"""
    short=text.split(":SHORTANSWER:")
    short= True if len(short)>1 else False
    regex=r'{:(.*?)#}'
    matchs=re.finditer(regex,text)
    rep=[]
    for match in matchs:
        rep.append(match.group())
    for i,r in enumerate(rep):
        text=text.replace(r,";")
    repclean=[]
    for r in rep:
        r=r.replace("{:SHORTANSWER:","").replace("{:MULTICHOICE:",'').replace("#",'').replace('}','')
        repclean.append(r)
    return {'question':text, 'reponse':repclean,'short_answer':short}

def extract_data(text):
	"""Pour chaque question cette fonction est appeller"""
	#si une question possed ce ci a son sein {: ce que il stock sa reponse dans la question
	if "{:" in text:

		tronc=text.split("{")
		question=[]
		reponse=[]
		for indice,block in enumerate(tronc):
			#parcourir les morceau de la question
			#separer la repose du morcau de la question la question est soit a gau
			#question={text:[reponse,reponse]}
			lsi=block.split("#}")
			if len(lsi) <=1:
				question.append(lsi[0])
			else:
				question.append(lsi[1])
			
				if ":SHORTANSWER:" in lsi[0]:
					rep=lsi[0]
					rep=rep.replace(":SHORTANSWER:","")
					if"%" in rep:
						repp=rep.split('%')
						reponse.append(repp[2])
				elif ":MULTICHOICE:" in lsi[0]:
					try:
						rep=lsi[0]
						rep=rep.replace(":MULTICHOICE:","").replace("#","")
						#chauqe block de text du reponse a plusieur reponse possibele...la reponse devient donc une liste de 
						#liste de reponse
						#extraction de la liste de reponse pour ce block de text
						listeAssertions=rep.split("~")
						repons=[]
						for rep_group in listeAssertions:
							repp=rep_group.split("%")
							repp.remove("")
							repons.append(repp[0]+":"+repp[1])
						reponse.append(repons)
					except Exception as exc:
						print(exc)
						reponse.append(lsi[0])
					
				else:
					reponse.append(lsi[0])

		return {'question':question, "reponse":reponse}

	else:
		return text      
def get_all_quiz():
    """Recuperer la liste des quiz depuis la base de donnees"""
    questions_db=Quizz.objects.all()
    data=[]
    #print(request.FILES['file'])
    for question in questions_db:
        question_dict={
        'id_quiz':question.id,
        'niveau':question.niveau,
        'matiere':question.matiere,
        'description':question.description,
        'auteur':question.user,
        'mot_cles':question.motCles,
        'date':question.date
        }
        data.append(question_dict)
    return data

def get_question(quiz):

    questions=quiz.question_set.all()
    for q in questions:
        yield q
        
def get_users_quiz(user):
    """Recuperer la liste de quiz de cette utilisateur"""

    return Quiz.objects.filter(user=user)

def get_all_niveau():
    """recuperer tout les niveau dans la table de quiz"""
    n_liste=[q.niveau for q in Quizz.objects.all()]
    niveau=[]
    for n in n_liste:
        if n not in niveau:
            niveau.append(n)
    return niveau

def get_all_matiere():
    """recuperer tout la liste de matiere dans la table de quiz"""
    n_liste=[q.matiere for q in Quizz.objects.all()]
    matiere=[]
    for n in n_liste:
        if n not in matiere:
            matiere.append(n)
    return matiere

def get_keywords():
    """fabrique la liste de mots cles"""
    quiz=Quizz.objects.all()
    description=''
    keywords=[]
    for q in quiz:
        description+=q.motCles+";"
    description=description.split(";")
    for k in description:
        if "," in k:
            tmp_liste=k.split(",")
            for kk in tmp_liste:
                keywords.append(kk)
        else:
            keywords.append(k)
    #print(keywords)
    return keywords


def get_all_auteur():
    """Retourne la liste des auteurs de quiz"""
    auteur=Quizz.objects.all()
    auteur_liste=[]
    for k in auteur:
        if k.user not in auteur_liste:
            auteur_liste.append(k.user)
    return auteur_liste
def parse_question(path,quiz):
    """Extrait les questionaire du fichier"""
    try:
        data=ParseXml(path)
        question_liste=data.get_question_liste()
        print(len(question_liste))
        for question in question_liste:
            q=quiz.question_set.create(question_type=question['question_type'],question_text=question['titre_question'],question_image=question['link_image'],question_name=question['name_of_question'],question_externallink=question['externallink'])
            q.save()
            for e in question['answer']:
                ans=q.answer_set.create(answer_fraction=e['fraction'],answer_text=e['text'])
                ans.save()
        return 0

    except Exception as exc:
        print(exc)
        return 1
def load_questions(model):
    """Modifie le nom du fichier"""
    basefile=settings.MEDIA_ROOT
    try:
        oldfile_path=os.path.join(basefile,str(model.xmlfile))
        newPath=os.path.join(basefile,os.path.dirname(str(model.xmlfile)), str(model.id)+".xml")
        try:
            os.rename(oldfile_path,newPath)
            model.numFichier=model.id
            model.save()
        except Exception as exc:
            print(exc)
            return 1
        r=parse_question(newPath,model)
        if r == 0:
            return 0
        else:
            return 1
    except Exception as exc:
        print(exc)
        return 1

def save_quiz(request):
    """Enregistrer le quiz contenu dans le request"""
    try:
        form=AddQuizForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            modelInstance=form.save(commit=False)
            #enregistrement des entetes
            user_session=request.session['username']
            user=User.objects.get(username=user_session)
            modelInstance.user=user
            modelInstance.auteur=str(user)
            modelInstance.date=timezone.now()
            modelInstance.save()
            r=load_questions(modelInstance)
            if r == 0:
                return 0
            else:
                return 1


    except Exception as exc:
        print(exc)
        return 1

def alread_exist(question_text):
    #checking if question_text alread in banque de question table
    try:
        question=BanqueQuestion.objects.get(question_text=question_text)
        return True
    except Exception as exc:
        print(exc)
        return False
def refresh_q_banque():
    print("Mis a jours de la banque de question en cours.....")
    #getting all quiz
    count=0
    quiz=Quizz.objects.all()
    for q in quiz:
        #getting questions list
        q_liste=q.question_set.all()
        #save question on database
        for qst in q_liste:
            #alread exist
            if not alread_exist(qst.question_text):
                #save question to banque question
                bqst=BanqueQuestion(niveau=q.niveau,matiere=q.matiere,idQuiz=q.id,idUser=q.user.id,typeQuestion=qst.question_type, auteur=str(q.user),modifications=0,datePub=q.date,question_text=qst.question_text)
                bqst.save()
                #add answer
                answer=qst.answer_set.all()
                for ans in answer:
                    cc=bqst.bqanswer_set.create(answer_fraction=ans.answer_fraction,answer_text=ans.answer_text)
                    bqst.save()
                count+=1
                print("[{} questions] Saved".format(count))
    print("Mis ajours terminer Ok!")


def filter_by_niveau(niveau):
    """Recuperer la liste de tout les qui dont dont le niveau est niveau"""

    questions_db=Quizz.objects.filter(niveau=niveau)
    data_request=[]
    for q in questions_db:
        #user=User.objects.get(username=q.user)#recuperer l'user de ce quiz depuis la table user.
        data_question_liste={}
        data_question_liste['id_quiz']=q.id
        #idd=Quiz.objects.get(matiere=q.quiz)
        data_question_liste['matiere']=q.matiere
        data_question_liste['niveau']=q.niveau
        data_question_liste['description']=q.description
        data_question_liste['auteur']=str(q.user)
        data_question_liste['mot_cles']=q.motCles
        data_question_liste['date']=q.date
        data_request.append(data_question_liste)
    return data_request


def filter_by_matiere(matiere):
    """Recuperer la liste de tout les qui dont dont le niveau est niveau"""

    questions_db=Quizz.objects.filter(matiere=matiere)
    data_request=[]
    for q in questions_db:
        #user=User.objects.get(username=q.user)#recuperer l'user de ce quiz depuis la table user.
        data_question_liste={}
        data_question_liste['id_quiz']=q.id
        #idd=Quiz.objects.get(matiere=q.quiz)
        data_question_liste['matiere']=q.matiere
        data_question_liste['niveau']=q.niveau
        data_question_liste['description']=q.description
        data_question_liste['auteur']=str(q.user)
        data_question_liste['mot_cles']=q.motCles
        data_question_liste['date']=q.date
        data_request.append(data_question_liste)
    return data_request


def filter_by_auteur(auteur):
    """Recuperer la liste de tout les qui dont dont le niveau est niveau"""
    userr=User.objects.get(username=auteur)
    questions_db=Quizz.objects.filter(user=userr)
    data_request=[]
    for q in questions_db:
        #user=User.objects.get(username=q.user)#recuperer l'user de ce quiz depuis la table user.
        data_question_liste={}
        data_question_liste['id_quiz']=q.id
        #idd=Quiz.objects.get(matiere=q.quiz)
        data_question_liste['matiere']=q.matiere
        data_question_liste['niveau']=q.niveau
        data_question_liste['description']=q.description
        data_question_liste['auteur']=str(q.user)
        data_question_liste['mot_cles']=q.motCles
        data_question_liste['date']=q.date
        data_request.append(data_question_liste)
    return data_request


def filter_by_word(mot_cles):
    """Recuperer toutes les questions contenant le mot cle"""
    try:
        quizs=Quizz.objects.all()
        data_request=[]
        for q in quizs:
            if (mot_cles in q.description) or (mot_cles in q.motCles) or (mot_cles in str(q.user)) or (mot_cles in q.matiere) or (mot_cles in q.niveau):
                
                data_question_liste={}
                data_question_liste['id_quiz']=q.id
                #idd=Quiz.objects.get(matiere=q.quiz)
                data_question_liste['matiere']=q.matiere
                data_question_liste['niveau']=q.niveau
                data_question_liste['description']=q.description
                data_question_liste['auteur']=str(q.user)
                data_question_liste['mot_cles']=q.motCles
                data_question_liste['date']=q.date
                data_request.append(data_question_liste)
        return data_request
    except Exception as exc:
        print(exc)
        return []
    return []




def save_question(question,q_objet):
    c=q_objet.question_set.create(question_type=question['question_type'],question_text=question['question_titre'],question_image=question['question_image'],question_name=question['question_name'],question_externallink=question['question_externlink'])
    for enswer in question['question_answer']:
        c.answer_set.create(answer_fraction=enswer['fraction'], answer_text=enswer['text'])

    q_objet.save()
    c.save()