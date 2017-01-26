from django.shortcuts import render, redirect
from django.urls import reverse
from collections import defaultdict
from django.http import JsonResponse
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from imdb import IMDb
import json
from django.shortcuts import render
from models import Search
import os
import errno


def search_box(request):
	if request.method == 'GET':
		print request.GET['attr']
		print request.GET['search_term']
		recent_search = Search(search_term=request.GET['search_term'].replace(" ",""),attribute=request.GET['attr'])
		recent_search.save()
		print "Saved Successfully"
		if request.GET['attr']=='movies':
			search_movie = request.GET['search_term'].replace(" ","")
			#print '/movie_search/'+search_movie+'/'
			return HttpResponseRedirect ('/moviesearch/'+search_movie+'/')
		else:
			search_actor = request.GET['search_term'].replace(" ","")
			return HttpResponseRedirect ('/actorsearch/'+search_actor+'/')

def movie_search (request, search_movie):
	#print 
	ia = IMDb()
	movie_list = ia.search_movie(search_movie)
	movie_info = []
	for i in movie_list:
		movie_info.append({'id':i.getID(),'name':i['title'],'kind':i['kind']})
	print movie_list
	return render(request, 'imdbapp/moviesearch.html', {'movie_list':movie_info,'search_term':search_movie})

def actor_search (request, actor):
	ia = IMDb()
	actor_list = ia.search_person(actor)
	actor_info = []
	for i in actor_list:
		actor_info.append({'id':i.getID(),'name':i['name']})
	print type(actor_info)
	return render(request, 'imdbapp/actorsearch.html', {'actor_info':actor_info,'search_term':actor})

def graph_json (request, id):
	ia = IMDb()
	leo = ia.get_person(str(id))
	print leo
	if leo.has_key('actor') or leo.has_key('actress'):
		gender = 'actor' if leo.has_key('actor') else 'actress'
		movies = leo['actor']
		movies_id = []
		for i in movies[:5]:
			movies_id.append(ia.get_movie(str(i.getID())))
		network = defaultdict(lambda:0)
		for i in movies_id:
			for j in i['cast'][:5]:
				if j!=leo:
					network[str(j)]+=1
		json_data = {
			"nodes":[],
			"links":[]
		}

		json_data["nodes"].append({"name":leo['name'],"group":1})
		for i in network:
			json_data["nodes"].append({"name":i,"group":2})
		count = 1
		for i in network:
			json_data["links"].append({"source":0,"target":count,"weight":network[i]})
			count+=1
		json_response = JsonResponse(json_data)
		return HttpResponse(json_response)
	else:
		return HttpResponseRedirect("Actor Or Actress Data Missing")

def actor_specific (request,actor_id):
	ia = IMDb()
	actor = ia.get_person(actor_id)
	movie_list = []
	if actor.has_key('actor') or actor.has_key('actress'):
		gender = 'actor' if actor.has_key('actor') else 'actress'	
		for i in actor[gender]:
			movie_list.append({'id':i.getID(),'title':i['title']})

		biography = actor['mini biography'] if actor.has_key('mini biography') else " "
		birthday = actor['birth date'] if actor.has_key('birth date') else " "
		image = actor['full-size headshot'] if actor.has_key('full-size headshot') else " "
		birth_notes = actor['birth notes'] if actor.has_key('birth notes') else " "
		actor_info = {'id':actor_id,'name':actor['name'],'birth_notes':birth_notes,'birthday':birthday,'movies':movie_list,'image':image,'biography':biography}
		
		return render(request,'imdbapp/actor.html',{'actor_info':actor_info})
	else:
		return HttpResponse("The particular actor details isn't present in the database \n Thank You")

def movie_specific (request,movie_id):
	ia = IMDb()
	movie = ia.get_movie(str(movie_id))
	cast = []
	for i in movie['cast'][:5]:
		cast.append({'id':i.getID(),'name':i['name']})
	movie_info = {'id':movie_id,'name':movie['title'],'rating':movie['rating'],'year':movie['year'],'cast':cast}
	print movie_info
	return render(request,'imdbapp/movie.html',{'movie':movie_info})

def homepage (request):
	ia = IMDb()
	recent_search = Search.objects.all()[:5]

	return render(request,'imdbapp/index.html',{'recent_search':recent_search})

