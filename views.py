from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from trips.models import Post
from trips.models import Article
import os
import subprocess, sys
from subprocess import Popen, PIPE, STDOUT
from django import forms

class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ['title', 'content', ]

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['iden', 'content', ]

def creates(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():
			new_article = form.save()
			Post.objects.create(iden=new_article.title,content=new_article.content)
			return HttpResponseRedirect('/index/'+new_article.title)

	form = ArticleForm()
	return render(request, 'create_article.html', {'form': form})

def index(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():
			new_article = form.save()
			process.stdin.write(str.encode(new_article.content))
			print (new_article.content+"\t\n")
		#	print(process.stdout.readline())
		#	process.stdout.close()
			return HttpResponseRedirect('/request/')

	form = ArticleForm()
	global process 
	process = Popen('python C:/Users/aa/proj_DB/mysite/Chatbot-master/chatbot.py', stdin=PIPE)
	#for line in iter(process.stdout.readline,''):
	#	print("test:", line.rstrip())
	#	if line.rstrip() == b'[Console] Initialized successfully :>':
	#		print("I am break")
	#		break
	#subprocess.Popen('python C:/Users/aa/proj_DB/mysite/Chatbot-master/chatbot.py', stdin=PIPE, stderr=STDOUT,executable=None, shell=False)
	return render(request, 'create_article.html', {'form': form})


def request_data(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():
			new_article = form.save()
			process.stdin.write(str.encode(new_article.content+"\t\n"))
	#		print(process.stdout.readline())
	#		process.stdout.close()
			return HttpResponseRedirect('/request/')

	form = ArticleForm()
	#subprocess.Popen('python C:/Users/aa/proj_DB/mysite/Chatbot-master/chatbot.py', stdin=PIPE, stderr=STDOUT,executable=None, shell=False)
	return render(request, 'get.html', {'form': form})
	
def submit(request, pk, data):
	print(pk)
	print(data)
	post = Post.objects.filter(iden=pk)
	if len(post) == 0:
		Post.objects.create(iden=pk,content=data)
	return render(request, 'submit.html', {'post': pk,'data': data})
