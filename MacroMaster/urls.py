"""MacroMaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
<<<<<<< HEAD:MasterMacro/MasterMacro/urls.py
from django.conf.urls import include, url
=======
from django.conf.urls import *
>>>>>>> 21ade5d02e55fe8cccf5def1405e3af15225fbde:MacroMaster/urls.py
from django.contrib import admin
from django.contrib.auth.views import login, logout
from users.views import SignUpView
from polls.views import search
admin.autodiscover()

urlpatterns = [
<<<<<<< HEAD:MasterMacro/MasterMacro/urls.py
    url(r'^mmapp/', include('mmapp.urls')),
    url(r'^admin/', admin.site.urls),
=======
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', include(admin.site.urls)),
]


urlpatterns += [
    url(r'^login/$', login, name='user_login'),
    url(r'^logout/$', logout, name='user_logout'), 
    url(r'^signup$', SignUpView.as_view(), name='user_signup'), 
>>>>>>> 21ade5d02e55fe8cccf5def1405e3af15225fbde:MacroMaster/urls.py
]
