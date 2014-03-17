from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'meals.views.home_page', name='home'),

	url(r'^meals/(\d+)/$', 'meals.views.view_arsenal', name='view_arsenal'),
	url(r'^meals/new$', 'meals.views.new_arsenal', name='new_arsenal'),
	url(r'^meals/(\d+)/new_entree$', 'meals.views.add_entree', name='add_entree'),

    #url(r'^admin/', include(admin.site.urls)),
)
