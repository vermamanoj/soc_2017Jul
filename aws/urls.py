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
    url(r'config', config),
    url(r'get_insecure_instances', get_insecure_instances, name="get_insecure_instances"),
    url(r'insecure_instance_acl_json', insecure_instance_acl_json),
    url(r'get_instance_acl_json/(i-\w+)$', get_instance_acl_json, name="get_instance_acl_json"),
    url(r'get_instance_acl/(i-\w+)$', get_instance_acl, name="get_instance_acl"),
    url(r'send_email', send_email, name="send_email"),
    url(r'secure_acl/(i-\w+)$', secure_acl, name="secure_acl"),
    # url(r'insecure_instance_acl', insecure_instance_acl_old),

]
