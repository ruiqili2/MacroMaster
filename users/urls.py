from django.conf.urls import include, url
import .views

urlpatterns = [
    url(r'^home$', views.get_user_home, name='home_user'),
  #  url(r'^signup$', views.signup, name='user_signup'),
]
