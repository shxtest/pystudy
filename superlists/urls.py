from django.conf.urls import include, url
from django.contrib import admin

#解析URL
urlpatterns = [
    # Examples:
    url(r'^$', 'lists.views.home_page', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
]
