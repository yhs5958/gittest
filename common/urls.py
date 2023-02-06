'''
파일명 : urls.py
설 명 :  로그인/로그 아웃
생성일 : 2023-02-06
생성자 : user
since 2023.01.09 Copyright (C) by KandJang All right reserved.
'''
from django.urls import path
from django.contrib.auth import views as auth_views


app_name='common'

urlpatterns = [
   #django.contrib.auth앱의 LoginView 클래스를 활용
   path('login/',auth_views.LoginView.as_view(template_name='common/login.html'),name='login')
]