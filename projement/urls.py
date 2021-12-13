"""projement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from developer.views import DeveloperList, DeveloperDetail
from company.views import CompanyList, CompanyDetail
from project.views import ProjectCreate, ProjectUpdate, ListCompanyProjects, TagCreate, TagUpdate, ProjectFile,\
    LogList
from users.views import LoginUser, RegisterUser, Logout

urlpatterns = [
    path('api/company', CompanyList.as_view()),
    path('api/company/<int:pk>', CompanyDetail.as_view()),
    path('api/developer', DeveloperList.as_view()),
    path('api/developer/<int:pk>', DeveloperDetail.as_view()),
    path('api/project', ProjectCreate.as_view()),
    path('api/project/<int:pk>', ProjectUpdate.as_view()),
    path('api/company/project/<int:company_id>', ListCompanyProjects.as_view()),
    path('api/tags', TagCreate.as_view()),
    path('api/tag/<int:pk>', TagUpdate.as_view()),
    path('api/project-export', ProjectFile.as_view()),
    path('api/register', RegisterUser.as_view()),
    path('api/login', LoginUser.as_view()),
    path('api/logout', Logout.as_view()),
    path('api/logs', LogList.as_view()),
    path('admin/', admin.site.urls),
]