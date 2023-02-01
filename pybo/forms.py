'''
파일명 : forms.py
설 명 : html form 관리
생성일 : 2023-02-01
생성자 : user
since 2023.01.09 Copyright (C) by KandJang All right reserved.
'''

from django import forms
from pybo.models import Question, Answer


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer #  사용할 Answer model

        fields = ['content'] #AnswerForm 사용할 Answer model 속성

        labels = {
            'content': '답변내용'

        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question #사용할 question model
        
        fields =['subject','content'] #QuestionForm사용할 question model의 속성

        labels ={    #subject->제목으로 변경
            'subject': '제목',
            'content': '내용',
        }