# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views


from mainapp.views import DataPreview, GetPagePostsAPI
from django.views.decorators.cache import cache_page
from action.api import UserDataDetail, UserDataList


urlpatterns = [
    url(
        r'^$',
        TemplateView.as_view(template_name='landing.html'),
        name='home'
    ),
    # url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('fbstats.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(
        r'^api-auth/', include(
            'rest_framework.urls', namespace='rest_framework')),
    url(
        r'^$',
        TemplateView.as_view(template_name='landing.html'),
        name='home'
    ),
    url(
        r'^preview/$',
        cache_page(60 * 60)(DataPreview.as_view()),
        name='data-preview'
    ),
    url(
        regex=r'^api/stats/$',
        view=GetPagePostsAPI.as_view(),
        name='api'
    ),
    url(
        r'^api/user-data/(?P<pk>[-\d]+)/$',
        UserDataDetail.as_view(),
        name='userdata_detail'
    ),
    url(
        r'^api/user-data/$',
        UserDataList.as_view(),
        name='userdata_list'
    ),
    url(
        r'^user-data/create/$',
        TemplateView.as_view(template_name="create.html")
    ),
    url(
        r'^user-data/update/$',
        TemplateView.as_view(template_name="update.html")
    ),

    # Your stuff: custom urls includes go here


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]