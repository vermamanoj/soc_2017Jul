"""gentelella URL Configuration

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
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index),
    url(r'config', qradar_config),
    url(r'^aql_query/$', run_aql_query),
    url(r'^events_category/$', qradar_events_category),
    url(r'^userBySourceIP/$', qradar_userBySourceIP),
    url(r'^dashboard1/$', qradar_dashboard1),
    url(r'^offenses/(\d+)/$', get_offenses),
    url(r'^write_offenses_to_es/$', write_offenses_to_es),

    url(r'^write_qradar_events_to_es/$', write_qradar_events_to_es),
    #Test URLs
    url(r'get_es_offenses/$', get_es_offenses),
    url(r'get_es_offenses/(\d+)$', get_es_offenses),
    url(r'^show_alerts/$', show_alerts),
    url(r'^xf_dns/$', xf_dns),
]
