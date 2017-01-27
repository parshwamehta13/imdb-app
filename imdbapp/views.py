from django.shortcuts import render, redirect
from django.urls import reverse
from collections import defaultdict
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from imdb import IMDb
import json
from django.shortcuts import render
from models import Search, Actor, Actor_Graph
import os
import errno

ia = IMDb()
# for local database ia = IMDb('sql',uri='mysql://imdb:password@localhost/imdb')


# Method for handling the search box. It calls the respective movie_search or actor_search methods
# The caching mechanism is also implemented to save the recent searches
def search_box(request):
	if request.method == 'GET':
		recent_search = Search(search_term=request.GET['search_term'].replace(" ",""),attribute=request.GET['attr'])
		recent_search.save()
		if request.GET['attr']=='movies':
			search_movie = request.GET['search_term'].replace(" ","")
			return HttpResponseRedirect ('/moviesearch/'+search_movie+'/')
		else:
			search_actor = request.GET['search_term'].replace(" ","")
			return HttpResponseRedirect ('/actorsearch/'+search_actor+'/')


# Method to handle the moviesearch url
def movie_search (request, search_movie):
	movie_list = ia.search_movie(search_movie)
	movie_info = []
	for i in movie_list:
		movie_info.append({'id':i.getID(),'name':i['title'],'kind':i['kind']})
	print movie_list
	return render(request, 'imdbapp/moviesearch.html', {'movie_list':movie_info,'search_term':search_movie})

# Method to handle the actorsearch url
def actor_search (request, actor):
	actor_list = ia.search_person(actor)
	actor_info = []
	for i in actor_list:
		actor_info.append({'id':i.getID(),'name':i['name']})
	print type(actor_info)
	return render(request, 'imdbapp/actorsearch.html', {'actor_info':actor_info,'search_term':actor})

# Returns a json response to construct the graph
# Caching machanism to save the already searched actor's graph json 
def graph_json (request, id):
	# try if the json is present in the database 
	try:
		a = Actor_Graph.objects.get(pk=id)
		jsonDec = json.decoder.JSONDecoder()
		print type(a.json_data)
		json_data = a.json_data
	
	# else fetch it from the http (or local database of IMDB)
	except:
		a = ia.get_person(str(id))
		if a.has_key('actor') or a.has_key('actress'):
			gender = 'actor' if a.has_key('actor') else 'actress'
			movies = a[gender]
			movies_id = []
			count = 0
			for i in movies:
				if count == 5:
					break
				movie = ia.get_movie(str(i.getID()))
				if movie.has_key('cast'):
					movies_id.append(movie)
					count+=1
			network = defaultdict(lambda:0)
			for i in movies_id:
				for j in i['cast'][:5]:
					if j!=a:
						network[str(j)]+=1
			json_data = {
				"nodes":[],
				"links":[]
			}

			json_data["nodes"].append({"name":a['name'],"group":1})
			for i in network:
				json_data["nodes"].append({"name":i,"group":2})
			count = 1
			for i in network:
				json_data["links"].append({"source":0,"target":count,"weight":network[i]})
				count+=1
			a = Actor_Graph(id,json.dumps(json_data))			
			a.save()
			json_data = JsonResponse(json_data)
			print "Instance Saved"
		else:
			return HttpResponseRedirect("Actor Or Actress Data Missing")
	return HttpResponse(json_data)

# Method to return the data of the actor
def actor_specific (request,actor_id):
	# Try if it is present in database 
	try:
		actor_info = Actor.objects.get(pk=actor_id)
		jsonDec = json.decoder.JSONDecoder()
		actor_info.movie_list = jsonDec.decode(actor_info.movie_list)

	# else fetch it from the http (or local database of IMDB)
	except:
		actor = ia.get_person(actor_id)
		movie_list = []
		if actor.has_key('actor') or actor.has_key('actress'):
			gender = 'actor' if actor.has_key('actor') else 'actress'	
			for i in actor[gender]:
				movie_list.append({'id':i.getID(),'title':i['title']})

			biography = actor['mini biography'][0] if actor.has_key('mini biography') else " "
			birthday = actor['birth date'] if actor.has_key('birth date') else " "
			image = actor['full-size headshot'] if actor.has_key('full-size headshot') else " " 	
			birth_notes = actor['birth notes'] if actor.has_key('birth notes') else " "
			actor_info = {'id':actor_id,'name':actor['name'],'birth_notes':birth_notes,'birthday':birthday,'movie_list':movie_list,'image':image,'biography':biography}

			a = Actor(actor_info['id'],actor_info['name'],gender,actor_info['biography'],actor_info['image'],actor_info['birth_notes'],json.dumps(actor_info['movie_list']),actor_info['birthday'])
			a.save()
			print "Actor Information Saves"
		else:
			return HttpResponse("The particular actor details isn't present in the database \n Thank You")
	return render(request,'imdbapp/actor.html',{'actor_info':actor_info})

# Method to return the data of the movie
def movie_specific (request,movie_id):
	movie = ia.get_movie(str(movie_id))
	cast = []
	for i in movie['cast'][:5]:
		cast.append({'id':i.getID(),'name':i['name']})
	rating = movie['rating'] if movie.has_key('rating') else 7.5
	year = movie['year'] if movie.has_key('year') else " "
	image = movie['full-size cover url'] if movie.has_key('full-size cover url') else " "
	plot = movie['plot'][0] if movie.has_key('plot') else " "
	genre = movie['genre'][0] if movie.has_key('genre') else " "
	movie_info = {'id':movie_id,'name':movie['title'],'rating':rating,'year':year,'cast':cast,'image':image,'plot':plot,'genre':genre}
	print movie_info
	return render(request,'imdbapp/movie.html',{'movie':movie_info})

# Method to handle the homepage of the App
def homepage (request):
	recent_search = Search.objects.all()[:5]
	return render(request,'imdbapp/index.html',{'recent_search':recent_search})

