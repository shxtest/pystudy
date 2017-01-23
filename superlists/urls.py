from django.conf.urls import include, url
from django.contrib import admin

#解析URL
urlpatterns = [
    # Examples:
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^lists/the-only-list-in-the-world/$', 'lists.views.view_list',
        name='view_list'),
    # url(r'^admin/', include(admin.site.urls)),
]
