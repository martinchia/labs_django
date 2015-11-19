from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
from books import views
admin.autodiscover()
#lalala#
urlpatterns = patterns('',
    ('^$',views.home),
    (r'^book/',views.books),
    (r'^author/$',views.author),
    (r'^delete/',views.delete),
    (r'^checkbook/',views.checkbook),
    url(r'^medias/(?P<path>.*)$', 'django.views.static.serve',\
    {'document_root': settings.MEDIA_ROOT },name="media"),
    # Examples:
    # url(r'^$', 'Lab3.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
