"""DiagnosticCentre URL Configuration

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
from django.conf.urls import url
from django.views import View
from django.conf import settings
from django.conf.urls.static import static

from home.views import (home, profile, test, appointments, 
							checkAvailability, cancel, staffview,
							addstaff, removestaff, upload, uploadrep, download, showreports)
from login.views import LoginHandler, LogoutHandler, RegisterUser
from admin.views import AdminLogin, managestaff


urlpatterns = [
	url(r'^$', home),
	url(r'^admin$', AdminLogin.as_view()),
	# url(r'^admin/logout$', AdminLogout.as_view()),
	url(r'^login$', LoginHandler.as_view()),
	url(r'^logout$', LogoutHandler.as_view()),
	url(r'^register/user$', RegisterUser.as_view()),
	url(r'^profile$', profile),
	url(r'^book/(?P<testname>[a-z,A-Z,0-9-,\w+/]+)/$', test),
	url(r'^appointments$', appointments),
	url(r'^checkavail/', checkAvailability),
	url(r'^managestaff/', managestaff.as_view()),
	url(r'^staffview/', staffview),
	url(r'^addstaff', addstaff),
	url(r'^cancel', cancel),
	url(r'^removestaff', removestaff),
	url(r'^upload/(?P<id>[a-z,A-Z,0-9-,\w+/]+)/$', upload),
	url(r'^uploadrep', uploadrep),
	url(r'^reports/', showreports),
	url(r'^download', download),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
