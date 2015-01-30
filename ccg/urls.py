from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

from main import Main 
from amf.gateway import gateway

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
	url(r'^getAllCards/?$', Main.getAllCards),
	url(r'^getAllHeros/?$', Main.getAllHeros),
	url(r'^getAllHeros2/?$', Main.getAllSystemAndUserHeros),
	url(r'^getAllHeros3/?$', Main.getSystemOrUserHerosById),
	
	url(r'^getRandHeros/?$', Main.getRandHeros),
	url(r'^getRandCards/?$', Main.getRandCards),
	url(r'^gateway/?$', gateway), 
)
