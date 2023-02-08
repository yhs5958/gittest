'''
파일명 : urls.py
설 명 : pybo 모든 URL과 view함수의 메핑 담당!
생성일 : 2023-01-25
생성자 : user
since 2023.01.09 Copyright (C) by KandJang All right reserved.
'''


from django.urls import path
from .views import question_views,answer_views,boot_views ,base_views

app_name = 'pybo'

urlpatterns = [
    #bash_view
    path('',base_views.index,name='index'), #view index로 메핑
    path('<int:question_id>/', base_views.detail, name='detail'),

    #answer
    path('answer/create/<int:question_id>/',answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/',answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/',answer_views.answer_delete, name='answer_delete'),

    #question
    path('question/create/',question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/',question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/',question_views.question_delete, name='question_delete'),

    #boot
    path('boot/menu/',boot_views.boot_menu, name='boot_menu'),
    path('boot/list/',boot_views.boot_list, name='boot_list'),
    path('boot/reg/',boot_views.boot_reg, name='boot_reg'),
    path('crawling/cgv/',boot_views.crawling_cgv, name='crawling_cgv'),
]
