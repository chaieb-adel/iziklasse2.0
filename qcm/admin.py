from django.contrib import admin
from qcm.models import Auth_group
from qcm.models import Quizz
from qcm.models import Question
from qcm.models import Answer
from qcm.models import Points
from qcm.models import BanqueQuestion
from qcm.models import Modification
from qcm.models import Upload_file,UserAccess,BqAnswer,Niveau,Matiere,SimQuiz


#,Points,Quiz,Answer




# Register your models here.
admin.site.register(Auth_group)
admin.site.register(Quizz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Points)
admin.site.register(BanqueQuestion)
admin.site.register(Modification)
admin.site.register(Upload_file)
admin.site.register(UserAccess)
admin.site.register(BqAnswer)
admin.site.register(Niveau)
admin.site.register(Matiere)
admin.site.register(SimQuiz)
