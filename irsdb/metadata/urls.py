"""irsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.urls import path, re_path
from metadata import views


urlpatterns = [
    path(r'forms.html', views.show_forms),
    path(r'about.html', views.show_about),
    re_path(r'parts/(?P<part>[\w\d]+).html$', views.show_part),
    re_path(r'groups/(?P<group>[\w\d]+).html$', views.show_group),
    re_path(r'xpath/(?P<xpath>.+).html', views.show_xpath),
    re_path(r'variable/(?P<db_name>[\w\d\_]+)\-(?P<variable_name>[\w\d]+).html$', views.show_variable),

]

