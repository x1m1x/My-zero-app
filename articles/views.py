from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Article, Comment

def index(request):
	latest_articles_list = Article.objects.order_by("-pub_date")[:5]

	context = {"latest_articles_list": latest_articles_list}

	return render(request, 'articles/list.html', context)

def detail(request, article_id):
	try:
		a = Article.objects.get(id=article_id)
	except:
		raise Http404("Статья не найдена!")

	comments = a.comment_set.all()

	context = {"article": a, "comments": comments}
	
	return render(request, 'articles/detail.html', context)

def leave_comment(request, article_id):
	try:
		a = Article.objects.get(id=article_id)
	except:
		raise Http404("Статья не найдена!")

	a.comment_set.create(author_name=request.POST['name'], comment_text = request.POST['text'])

	return HttpResponseRedirect(reverse("articles:detail", args=(a.id,) ) )