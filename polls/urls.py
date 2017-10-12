from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^home/', views.home, name='home'),
    url(r'^search_for$', views.search_page, name='explore'),
    url(r'^result$', views.search, name='search')
]