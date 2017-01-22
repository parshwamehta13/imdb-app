from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from imdb import IMDb
import json
from django.shortcuts import render


def movie_search (request, search_movie):
	#print 
	ia = IMDb()
	movie_list = ia.search_movie(search_movie)
	movie_info = []
	for i in movie_list:
		movie_info.append({'id':i.getID(),'name':i['title'],'kind':i['kind']})
	print movie_list
	return render(request, 'imdbapp/moviesearch.html', {'movie_list':movie_info})

def actor_search (request, actor):
	ia = IMDb()
	actor_list = ia.search_person(actor)
	actor_info = []
	for i in actor_list:
		actor_info.append({'id':i.getID(),'name':i['name']})
	print type(actor_info)
	return render(request, 'imdbapp/actorsearch.html', {'actor_info':actor_info})


def actor_specific (request,actor_id):
	ia = IMDb()
	actor = ia.get_person(actor_id, info=['filmography'])
	movie_list = []
	for i in actor['actor']:
		movie_list.append({'id':i.getID(),'title':i['title']})
	actor_info = {'id':actor_id,'name':actor['name'],'birth_notes':actor['birth notes'],'birthday':actor['birth date'],'movies':movie_list}
	#print actor_info
	return HttpResponse(actor_info)

def movie_specific (request,movie_id):
	ia = IMDb()
	movie = ia.get_movie(str(movie_id))
	cast = []
	for i in movie['cast'][:5]:
		cast.append({'id':i.getID(),'name':i['name']})
	movie_info = {'id':movie_id,'name':movie['title'],'rating':movie['rating'],'year':movie['year'],'cast':cast}
	return HttpResponse(movie_info)

