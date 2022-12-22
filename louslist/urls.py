"""louslist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('search/', TemplateView.as_view(template_name="search_page.html"), name='users-home'),
    path('search/users/', views.SearchUsersHomeView.as_view(), name='search_users_home_view'),
    path('search/users/results', views.SearchUsersResultsView.as_view(), name='search_users_results_view'),
    path('search/general', views.SearchGeneralResultsView.as_view(), name="search_general_results"),
    path('departments/', views.get_departments, name='all_departments'),
    #path('departments/<str:dept>', views.find_all_by_dept_v2, name='dept_page'),
    path('loadall/', views.loadall, name="loadall"),
    path('departments/<str:dept>', views.dept_page, name='dept_page'),
    path('departments/<str:dept>/<str:catalog_number>', views.course_page, name="course_page"),
    path('departments<str:dept>/<str:catalog_number>/<int:course_number>/', views.section_page, name="section_page"),
    path('section/save', views.save_section, name='save_section'),
    path('section/unsave', views.unsave_section, name='unsave_section'),
    path('section/', views.saved_sections, name="view_saved_sections"),
    #path('departments/<str:dept>/<str:cn>/<str:desc>/info', views.info, name='course_page'),
    path('register/', views.RegisterView.as_view(), name='users-register'),
    path('profile/', views.profile, name='users-profile'),
    path('login/', views.CustomLoginView.as_view(redirect_authenticated_user=True, template_name='login.html',
                                           authentication_form=views.LoginForm), name='login'),
    path('search/logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('password-change/', views.ChangePasswordView.as_view(), name='password_change'),
    path('search/saved_courses/', views.get_saved_courses, name='saved_courses'),
    path('instructors/<str:instr>', views.find_all_by_instructor, name="instructor_page"),
    path('catalog_number/<str:cn>', views.find_all_by_catalog_number, name="catalog_number_page"),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    
    path('profile/save',views.friend_profile, name='friend_user'),
    path('profile/unsave',views.unfriend_profile, name='unfriend_user'),
    path('profile/<str:username>', views.ProfileDetailView.as_view(), name="profile_detail_view"),
    path('comment/', views.make_comment, name="make_comment"),
    path('friends/',views.FriendsView.as_view(), name='friends_view'),
]
