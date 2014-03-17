from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'meals.views.home_page', name='home'),
	url(r'^meals/the-only-mealplan-in-the-world/$', 'meals.views.view_meals', name='view_meals'),
	url(r'^meals/new$', 'meals.views.new_meals', name='new_meals'),


    #url(r'^admin/', include(admin.site.urls)),
)
