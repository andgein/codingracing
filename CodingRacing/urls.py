from django.conf.urls import include, url
from django.contrib import admin

import CodingRacing.views

urlpatterns = [url(r'^$', CodingRacing.views.index, name='index'),
               url(r'^auth$', CodingRacing.views.auth, name='auth'),
               url(r'^logout$', CodingRacing.views.logout, name='logout'),

               url(r'^scoreboard$', CodingRacing.views.scoreboard, name='scoreboard'),

               url(r'^training$', CodingRacing.views.training, name='training'),
               url(r'^training/start$', CodingRacing.views.training_start, name='training_start'),
               url(r'^training/(\d+)/code\.png$', CodingRacing.views.training_code, name='training_code'),
               url(r'^training/(\d+)/update$', CodingRacing.views.training_update, name='training_update'),
               url(r'^training/(\d+)/finish$', CodingRacing.views.training_finish, name='training_finish'),

               url(r'^contest/enjoy$', CodingRacing.views.contest_enjoy, name='contest_enjoy'),
               url(r'^contest/(\d+)/check$', CodingRacing.views.contest_check, name='contest_check'),
               url(r'^contest/(\d+)/code\.png$', CodingRacing.views.contest_code, name='contest_code'),
               url(r'^contest/(\d+)/update$', CodingRacing.views.contest_update, name='contest_update'),
               url(r'^contest/(\d+)/finish$', CodingRacing.views.contest_finish, name='contest_finish'),
               url(r'^contest/(\d+)$', CodingRacing.views.contest, name='contest'),

               url(r'^manage/?$', CodingRacing.views.manage, name='manage'),
               url(r'^manage/create$', CodingRacing.views.manage_create, name='manage_create'),
               url(r'^manage/contest/(\d+)$', CodingRacing.views.manage_contest, name='manage_contest'),
               url(r'^manage/contest/(\d+)/start$', CodingRacing.views.manage_start, name='manage_start'),
               url(r'^manage/contest/(\d+)/status$', CodingRacing.views.manage_status, name='manage_status'),

               url(r'^admin/', include(admin.site.urls))
               ]
