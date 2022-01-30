from django.contrib import admin
from django.urls import path,re_path
from django.urls.conf import include
from qcm import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Menu    
    path('',views.DashboardView.as_view(),name='dashboard'),# Dashboard 
    path('manager/',views.ManagerView.as_view(),name='manager' ),
    path('teacher/',views.TeacherView.as_view(),name='teacher'),
    path('student/', views.StudentView.as_view(),name='student'),
    #second niveau route
    path('manager/addquestion/<int:id_quiz>', views.ManagerAddQuestionView.as_view(), name='manager_add_question'),
    path('student/showquiz/<int:id_quiz>', views.StudentShowQuiz.as_view(), name='student_show_quiz'),
    path('manager/delete_quiz/<int:id_quiz>', views.DeleteQuizView.as_view(), name='delete_quiz'),
    path('manager/edit_quiz/<int:id_quiz>', views.EditQuizView.as_view(), name='edit_quiz'),
    path('manager/show_quiz/<int:id_quiz>', views.ShowQuizView.as_view(), name='show_quiz'),
    path('manager/reusemodel/<int:id_quiz>', views.ReUseView.as_view(), name='reuse_quiz'),
    path('manager/doquiz/<int:id_quiz>', views.DoQuizView.as_view(), name='do_quiz'),
    path('manager/delete_quest/<int:id_question>', views.DelQuestView.as_view(), name='del_quest'),
    path('manager/show_question/<int:indice_question>', views.ShowQuestionView.as_view(), name='show_question'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)