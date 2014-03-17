from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'meals.views.home_page', name='home'),

	url(r'^meals/', include('meals.urls')),

    #url(r'^admin/', include(admin.site.urls)),
)
