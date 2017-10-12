from django.conf.urls import include, url

from .views import SignUpView

urlpatterns = [
    url(r'^home$', views.get_user_home, name='home_user'),
    url(r'^signup$', SignUpView.as_view(), name='user_signup'),
]
