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
    re_path(r'xpath(?P<xpath>.+)\/+', views.show_xpath),
    #re_path(r'form/(?P<form>[\w\d]+)\/$', views.show_form),
    path(r'forms/', views.show_forms),
    re_path(r'parts/(?P<part>[\w\d]+)\/$', views.show_part),
    re_path(r'groups/(?P<parent_sked>[\w\d]+)/(?P<group>[\w\d]+)\/$', views.show_group),

    #re_path(r'variable/(?P<variable>.+)\/+$', views.show_variable),

]

