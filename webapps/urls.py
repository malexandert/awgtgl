from django.conf.urls import patterns, include, url
from django.contrib import admin

from awgtgl.forms import *

urlpatterns = patterns('',

	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'awgtgl.views.home', name='home'),
	url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'awgtgl/login.html'}, name='login'),
	url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
	url(r'^register$', 'awgtgl.views.register', name='register'),
	url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'awgtgl.views.confirm_registration', name='confirm'),
	url(r'^pathfinder$', 'awgtgl.views.pathfinder', name='pathfinder'),
	url(r'^make_journal$', 'awgtgl.views.make_journal', name='make_journal'),
	url(r'^write/(?P<id>\d+)$', 'awgtgl.views.write', name='write'),
	url(r'^journals$', 'awgtgl.views.journals_hub', name='journals'),
	url(r'^journal/(?P<id>\d+)$', 'awgtgl.views.view_journal', name='view_journal')
)
