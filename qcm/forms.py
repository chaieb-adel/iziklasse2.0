from django import forms
from qcm.models import Upload_file,Quizz,Niveau,Matiere


"""class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField(help_text='',widget=forms.FileInput(attrs={'class':'form-control form-control-sm','id':'formFileSm','accept':'.xml'}))"""


class UploadFileForm(forms.ModelForm):

    class Meta:
        model=Upload_file
        fields = ['xmlfile',]
        widgets={

            'xmlfile':forms.FileInput(attrs={'class':'form-control form-control-sm','id':'formFileSm','accept':'.xml'}),
        }

class AddQuizForm(forms.ModelForm):
    

    class Meta:
        model = Quizz
        fields = ['niveau','matiere','description','motCles','xmlfile']


        widgets = {
            'niveau':forms.Select(attrs={'class':'form-select form-control-sm','id':"niveau-name"},choices=[]),
            #'niveau': forms.Textarea(attrs={'class':'form-control form-control-sm','cols': 80,'rows': 1,'id':"niveau-name", 'data-toggle':'dropdown','aria-haspopup':'true','aria-expanded':'false'}),
            #'matiere': forms.Textarea(attrs={'class':'form-control form-control-sm','cols': 80,'rows': 1,'id':"matiere-name"}),
            'matiere':forms.Select(attrs={'class':'form-select form-control-sm','id':"matiere-n ame"},choices=[]),
            'description': forms.Textarea(attrs={'class':'form-control form-control-sm','cols': 80, 'rows': 7,'id':"description-text"}),
            'motCles': forms.Textarea(attrs={'class':'form-control form-control-sm','cols': 80, 'rows': 1,'id':"motcles-text"}),
            'xmlfile':forms.FileInput(attrs={'class':'form-control form-control-sm','id':'formFileSm','accept':'.xml'}),
        }
    def __init__(self, *args, **kwargs):
        super(AddQuizForm, self).__init__(*args, **kwargs)
        self.fields['niveau'].widget.choices = [(n.niveau,n.niveau) for n in Niveau.objects.all()]
        self.fields['matiere'].widget.choices = [(n.matiere,n.matiere) for n in Matiere.objects.all()]

class AttachedFileForm(forms.ModelForm):

    class Meta:
        model=Upload_file
        fields = ['xmlfile',]
        widgets={

            'xmlfile':forms.FileInput(attrs={'class':'form-control form-control-sm','id':'formFileSm','accept':'.xml'}),
        }



"""class UploadQuestionForm(forms.ModelForm):

    class Meta:
        model=Upload_question
        fields = ['xmlfile',]
        widgets={

            'xmlfile':forms.FileInput(attrs={'class':'form-control form-control-sm','id':'formFileSm','accept':'.xml'}),
        }"""

