from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^profile/', views.get_user_home ,name='home_user'),
    url(r'^my_recipes/', views.get_my_recipes),
    url(r'^my_favorites/', views.get_my_favorites),
    url(r'^comment/', views.comment),
    url(r'^recommend/', views.recommend),
    url(r'^add_to_my_favorite/', views.add_to_favorites),
    url(r'^del_from_my_favorite/', views.del_from_favorites),
    url(r'^change_page', views.go_to_change_page),
    url(r'^change_my_recipe', views.change_my_recipe),
    url(r'^delete', views.delete_recipe),
    url(r'^rating', views.rate_recipe),
    url(r'^change_my_profile', views.go_to_change_profile),
    url(r'^editProfile', views.edit_profile),
]
