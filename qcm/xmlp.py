import xml.etree.ElementTree as ET
import xmltodict,untangle
from bs4 import BeautifulSoup
from django.conf import settings
import random
from bs4 import BeautifulSoup
import os
import base64
from shutil import move
import time
import xml.etree.ElementTree as ET
import re


#file_liste=[file for file in os.listdir('./xmlfile/')]#Acoustique7a3024fa6dda3a7ae2c459096a80a8cc.xml','AIPR-OPERATEUR-20210a74283806ea4848f042e5150cf49764.xml','Fonction-2nd-degre63362eca340200e8c3962ce4b8081ffe.xml','INTERSTELLAR-Filmc96997581f0edb7178a8e36268c921ce.xml']
#parse file



def b64_to_image(base64_code):
		"""Extract the image from question"""
		try:
			
			name_of_image=str(random.randint(0,100000000000))+".png"
			sav_as=os.path.join(settings.MEDIA_ROOT,"images",name_of_image)
			path_root=os.path.join("images",name_of_image)
			with open(sav_as,'wb') as f:
				f.write(base64.b64decode((base64_code)))
			return path_root
		except Exception as exc:
			print(exc)
			return 1

def extract_data(text):
	"""Por chaque question cette fonction est appeller
	cxvcxvxcvxcv    {:SHORTANSWER:%100%adel dfff#}  dsfsdfdsf  
	{:SHORTANSWER:%100%22222#}      sdfsfsdfdsdffdsf00 {:SHORTANSWER:%100%33333333#}
	vvxcvxcvxcv   {
		:MULTICHOICE:%100%xcvcxvxcv#~%0%dsfdsfd#~%0%333333#~%0%2222222#
		} 
		 vgsfdsfdfsdfsd {:MULTICHOICE:%0%xcvcxvxcv#~%0%dsfdsfd#~%0%333333#~%100%2222222#}    d
		sfsdfsd dffsfsdf   {:MULTICHOICE:%0%xcvcxvxcv#~%0%dsfdsfd#~%100%333333#~%0%2222222#}
		vvxcvxcvxcv   {
		:MULTICHOICE:%100%xcvcxvxcv#~%0%dsfdsfd#~%0%333333#~%0%2222222#
		} 
		 vgsfdsfdfsdfsd machin truc {:MULTICHOICE:%0%xcvcxvxcv#~%0%dsfdsfd#~%0%333333#~%100%2222222#}    d
		sfsdfsd dffsfsdf   {:MULTICHOICE:%0%xcvcxvxcv#~%0%dsfdsfd#~%100%333333#~%0%2222222#}
	probleme n1 : extraitre des reponnse dans cette question sans la deteriorer tout en laissant de repere pour chaque 
	reponse.
	"""
	text=text.replace('0xa0','')
	question_liste=[]
	q_data=[]
	reponse_liste=[]
	if "{:SHORTANSWER:" in text:
		regex=r"%[0-9]*%[a-zA-Z0-9]*( |[a-zA-Z0-9])*"
		reponse=re.finditer(regex,text)
		for match in reponse:
			reponse_liste.append(match.group())

		regex2=r"[a-zA-Z0-9]*( |{)"
		question=re.finditer(regex2,text)
		question_liste=[]
		for match in question:
			question_liste.append(match.group())
		reponse="xd".join(reponse_liste)
		q_liste_clean=[]
		for bribe in question_liste:
			if not (bribe in reponse):
				if len(bribe)>1:
					q_liste_clean.append(bribe)
		#q_liste_clean
		#reponse_liste
		"""
		[{
			'bribe_text':{
				'fraction':'100',
				'text':'shebang'
			}
		},]"""
		bribe_dic={}
		for indice,bribe in enumerate(q_liste_clean):
			
			rep=reponse_liste[indice]
			rep=rep.split("%")
			bribe_dic.setdefault(bribe,{
				'fraction':rep[1],
				'text':rep[2]
				})
			q_data.append(bribe_dic)
		#return q_data
			

	elif "{:MULTICHOICE:" in text:
		"""vvxcvxcvxcv   {
		:MULTICHOICE:%100%xcvcxvxcv#~%0%dsfdsfd#~%0%333333#~%0%2222222#
		} 
		 vgsfdsfdfsdfsd {:MULTICHOICE:%0%xcvcxvxcv#~%0%dsfdsfd#~%0%333333#~%100%2222222#}    d
		sfsdfsd dffsfsdf   {:MULTICHOICE:%0%xcvcxvxcv#~%0%dsfdsfd#~%100%333333#~%0%2222222#}
		
		"""
		"""
		[{
			'bribe_text':[{
				'fraction':'100',
				'text':'shebang'
			},]
		},]"""
		q_data=[]#ensemble de morceau pour cette question
		qustion={}#le morceau en cours de traitement
		question_liste=[]
		regex2=r"[a-zA-Z0-9]*( |{)"
		question=re.finditer(regex2,text)
		question_liste=[]
		for match in question:
			print(len(match))
			if len(match)>2:
				question_liste.append(match.group())
		print(question_liste)


		"""#Extraction reponse
		regex=r"%[0-9]*%[a-zA-Z0-9]*( |[a-zA-Z0-9])*"
		reponse=re.finditer(regex,text)
		for match in reponse:
			reponse_liste.append(match.group())

		reponse="xd".join(reponse_liste)
		q_liste_clean=[]
		for bribe in question_liste:
			if not (bribe in reponse):
				if len(bribe)>1:
					q_liste_clean.append(bribe)
		#q_liste_clean
		#reponse_liste
		bribe_dic={}
		for indice,bribe in enumerate(q_liste_clean):
			
			rep=reponse_liste[indice]
			rep=rep.split("%")
			bribe_dic.setdefault(bribe,{
				'fraction':rep[1],
				'text':rep[2]
				})
			q_data.append(bribe_dic)
		#return q_data
	else:
		return text"""

class ParseXml():

	def __init__(self,file):
		self.xml_file=file#le lien vers le fichier xml
		try:
			self.file_tree=ET.parse(self.xml_file)#file_tree parsed
			self.dom_root=self.file_tree.getroot()#dom root
		except Exception as exc:
			print(exc)

	def get_metadata(self):
		"""Recuperation des metadata
		metadata={
		"size_of":'',
		"name_of":'',
		"time_add":'',
		"time_modif":'',
		"link_file":''
		}"""
		abs_path=self.xml_file
		status=os.stat(self.xml_file)

		modificationTime = time.strftime('%d/%m/%Y a %H:%M', time.localtime(os.path.getmtime(abs_path)))
		createTime=time.strftime('%d/%m/%Y a %H:%M', time.localtime(os.path.getctime(abs_path)))
		size=os.path.getsize(abs_path)
		metadata={
		"size_of":"{} Kbs".format(size/1000),
		"name_of":self.xml_file,
		"time_add":createTime,
		"time_modif":modificationTime,
		"link_file":abs_path
		}
		return metadata

	def get_header(self):
		"""Recuperation de l'entete s'il ya en 
		header={
			"niveau":'',
			"matiere":'',
			"description":'',
			"mot_cles":'',
			"auteur":'',
			"file_indice":'',
			"numerotation_answ":''
		}"""
		header={}
		try:
			head=self.dom_root.find('question')
			if head.attrib['type'] == 'category':
				try:
					h_contanier=head.find('category')
					text_in=h_contanier.find('text')
					text_in=text_in.text.replace("<infos>","").replace("</infos>","")
					tmp_liste=text_in.split("</")
					name=tmp_liste[0].replace("<name>","")
					header['name']=name.replace("\n","").replace("\t","")
					try:
						numerotation_answ=tmp_liste[1].replace("name><answernumbering>","")
						header['numerotation_answ']=numerotation_answ
						
					except Exception as exc:
						header['numerotation_answ']=None
					try:
						niveau=tmp_liste[2].replace("answernumbering><niveau>","")
						header['niveau']=niveau
					except Exception as exc:
						header['niveau']=''
					try:
						matiere=tmp_liste[3].replace("niveau><matiere>","")
						header['matiere']=matiere
					except:
						header['matiere']=''

					return header
				except Exception as exc:
					return 1
			else:
				return 1
		except Exception as exc:
			return 1

	def get_question_liste(self):
		"""Recuperer la liste de question du quz"
		question ={
			"name_of_question":'',
			"titre_question":'',
			"type_question":'',
			"link_image":'',
			"external_link":'',
			"reponses":[]
		}"""
		question_liste=[]#liste de tout les questions du quiz
		
		
		try:
			body=self.dom_root.findall('question')
			print("Nombre de question {}".format(len(body)))
			for q in body:
				question={}
				question['answer']=[]
				#extraction des question
				if q.attrib['type'] != 'category':
					#extract type
					try:
						question['question_type']=q.attrib['type']
						#print(question['question_type'])
					except Exception as exc:
						question['question_type']=''
					#extract name
					try:
						name_of_question=q.find('name').find('text').text
						name_of_question=name_of_question.strip()
						question['name_of_question']=name_of_question
						#print(question['name_of_question'])
					except Exception as exc:
						question['name_of_question']=''
					
					#extract titre
					try:
						titre_of_question=q.find('questiontext')
						if titre_of_question.attrib['format'] == 'html':
							html=titre_of_question.find('text').text
							html=html.strip()
							cleantext = BeautifulSoup(html, "lxml").text
							question['titre_question']=cleantext
						else:
							question['titre_question']=titre_of_question
					except Exception as exc:
						print(exc)
						question['titre_question']=''
					#extract answer
					try:
						#Extraction de sous question du matching
						if question['question_type'] == "matching":
							try:
								subq=[]
								subquestion=q.findall('subquestion')
								for sub in subquestion:
									answer={}
									ans=sub.find('answer').find('text').text
									subtext=sub.find('text').text
									answer['fraction']=ans
									answer['text']=subtext
									question['answer'].append(answer)
									
							except Exception as exc:
								print("LIGNE 291",exc)
						else:
							answer_liste=q.findall('answer')
							for answerr in answer_liste:
								answer={}
								answer['fraction']=answerr.attrib['fraction']
								answer['text']=answerr.find('text').text.replace("\n","").replace("\t","")
								question['answer'].append(answer)
							

					except Exception as exc:
						print("LIGNE 302",exc)

					#extract image of question
					try:
						b64Code=q.find('image_base64').find('text').text
						b64Code=b64Code.replace("\n","").replace("\t","")
						bin_objet=b64Code.encode()
						image=b64_to_image(bin_objet)
						question['link_image']=image
					except Exception as exc:
						
						question['link_image']=''

					#extract external_link
					try:
						link=q.find('externallink').text
						question['externallink']=link if link != None else ''
					except Exception as exc:
						
						question['externallink']=''
					question_liste.append(question)
					del question


			return question_liste

		except Exception as exc:
			print("lIGNE 329",exc)
			return 1
			




if __name__=="__main__":
	#for file in file_liste:
	file='./10.xml'
	path=os.path.join(os.path.dirname(file),file)
	parsing_data=ParseXml(path)
	parsing_data.get_question_liste()
	del parsing_data
	time.sleep(5)
	
			