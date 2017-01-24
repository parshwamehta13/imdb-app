from django.conf.urls import url
from imdbapp import views

urlpatterns = [
    url(r'^moviesearch/(?P<search_movie>[a-z0-9]+)/$', views.movie_search,name='moviesearch'),
    url(r'^actorsearch/(?P<actor>[a-z0-9]+)/$', views.actor_search,name='actorsearch'),
    url(r'^actor/(?P<actor_id>[0-9]+)/$', views.actor_specific,name='actor'),
    url(r'^movie/(?P<movie_id>[0-9]+)/$', views.movie_specific,name='movie'),
    url(r'search/$',views.search_box,name='search_box'),
    url(r'^graph/(?P<id>[0-9]+)/$',views.graph_json,name='graph_json'),
]