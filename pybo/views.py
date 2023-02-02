from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils import timezone
from .models import Question
from .forms import QuestionForm, AnswerForm
from bs4 import BeautifulSoup
import requests
import logging


def crawling_cgv(request):
   ''' CGV 무비차트 '''
   url = 'http://www.cgv.co.kr/movies/?lt=1&ft=0'
   response = requests.get(url)

   context = {}
   if 200 == response.status_code:
      html = response.text
      # print('html:{}'.format(html))
      # box-contents
      soup = BeautifulSoup(html, 'html.parser')
      # 제목
      title = soup.select('div.box-contents strong.title')

      reserve = soup.select('div.score strong.percent span')
      # print('title:{}'.format(title))
      
      poster = soup.select('span.thumb-image img')

      title_list = []   #제목
      reserve_list = [] #예매율
      poster_list = [] #포스터
      for page in range(0, 7, 1):
         posterImg = poster[page]
         imgUrlPath = posterImg.get('src')  # <img src='' /> 에 접근
         # print('imgUrlPath:{}'.format(imgUrlPath))
         title_list.append(title[page].getText())
         reserve_list.append(reserve[page].getText())
         poster_list.append(imgUrlPath)
         print('title[page]:{},{},{}'.format(title[page].getText()
                                             , reserve[page].getText()
                                             , imgUrlPath
                                             ))
         pass
      #화면에 title을 []전달
      context = {'title': title_list,'reserve':reserve_list,'poster':poster_list}
   else:
      print('접속 오류 response.status_code:{}'.format(response.status_code))
   pass

   return render(request, 'pybo/crawling_cgv.html', context)

def question_create(request):
   '''질문등록'''
   logging.info('1.request.method:{}'.format(request.method))
   if request.method == 'POST':
      logging.info('2.question_create post')
      #저장
      form = QuestionForm(request.POST)  #request.POST 데이터 (subject,content 자동 생성)
      logging.info('3.question_create post')
      # form(질문등록)이 유효하면
      if form.is_valid():
         logging.info('4.form.is_valid():{}'.format(form.is_valid()))
         question=form.save(commit=False) # subject, content만 저장(commit은 하지 않음)
         question.create_date = timezone.now()
         question.save() #날짜 까지 생성해서 저장(Commit)
         return redirect("pybo:index")
   else:
      form = QuestionForm()
   context = {'form': form}
   return render(request,'pybo/question_form.html',context)

#bootstrap list
def boot_menu(request):
   '''개발에 사용되는 임시 메뉴'''
   return render(request,'pybo/menu.html')
def boot_reg(request):
   '''bootstrap reg template'''
   return render(request,'pybo/reg.html')
def boot_list(request):
   ''' bootstrap template'''
   return render(request,'pybo/list.html')

def answer_create(request, question_id):
   '''답변등록'''
   logging.info('answer_create question_id:{}'.format(question_id))
   question = get_object_or_404(Question,pk=question_id)

   if request.method == 'POST':
      form = AnswerForm(request.POST)
      logging.info('1.request.method:{}'.format(request.method))
      if form.is_valid():
         logging.info('2.form.is_valid():{}'.format(form.is_valid()))
         answer = form.save(commit=False)# content만 저장(commit은 하지 않음)
         answer.create_date = timezone.now()
         answer.question    = question
         answer.save() #최종 저장
         return redirect('pybo:detail',question_id=question.id)
   else:
      return HttpResponseNotAllowed('Post만 가능 합니다.')

   #form validation
   context = {'question':question,'form':form}
   return render(request,'pybo/question_detail.html',context)

def detail(request,question_id):
   '''question 상세'''
   logging.info('1.question_id:{}'.format(question_id))
   #question=Question.objects.get(id=question_id)
   question = get_object_or_404(Question,pk=question_id)

   logging.info('2.question:{}'.format(question))
   context = {'question':question}
   return render(request,'pybo/question_detail.html',context)


def index(request):
   '''question 목록'''
   #list order create_date desc
   logging.info('index 레벨로 출력')
   #logging.info('index 레벨로 출력')
   question_list= Question.objects.order_by('-create_date') #order_by('-필드') desc, asc order_by('필드')
   #question_list = Question.objects.filter(id=99)  # order_by('-필드') desc, asc order_by('필드')
   context = {'question_list' : question_list}
   logging.info('question_list:{}'.format(question_list))
   
   return render(request,'pybo/question_list.html',context)


