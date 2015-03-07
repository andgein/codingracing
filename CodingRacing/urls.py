from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^$', 'CodingRacing.views.index', name='index'),
                       url(r'^training$', 'CodingRacing.views.training', name='training'),
                       url(r'^training/start$', 'CodingRacing.views.training_start', name='training_start'),
                       url(r'^training/(\d+)/update', 'CodingRacing.views.training_update', name='training_update'),
                       url(r'^training/(\d+)/finish', 'CodingRacing.views.training_finish', name='training_finish'),

                       url(r'^admin/', include(admin.site.urls)),
)
