""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from gentelella.core.views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^qradar/', include('qradar.urls')),
    url(r'^mcafee/', include('mcafee.urls')),
    url(r'^aws/', include('aws.urls')),
    url(r'^soc_elastic/', include('soc_elastic.urls')),
    #url(r'^$', TemplateView.as_view(template_name="c3_dashboard.html")),
    #url(r'^$', TemplateView.as_view(template_name="c3_dashboard.html")),
    url(r'^c3_dashboard', c3_dashboard),
    url(r'^ir_playbook_1', ir_playbook_1),
    url(r'^ir_playbook_2', ir_playbook_2),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^qradar_offense_list/$', qradar),
    url(r'^qradar_offenses/$', qradar_offesnes),
    url(r'^qradar_dashboard/$', qradar_dashboard),
    #url(r'^servicenow/$', servicenow),
    #url(r'^servicenow/(\w+)/(\w+)/$',servicenow),
    url(r'^qo/$', qo),
    url(r'^qo/(\d+)/$', qo),
    url(r'^qradar_connect/$', qradar_connect),
    url(r'^plugins/$', plugins),
    url(r'^admin/', admin.site.urls),
    url(r'^servicenow/', include('ServiceNow.urls')),
    url(r'^bokeh/$', bokeh),
    url(r'^bokeh_json/$', bokeh_json),
]

