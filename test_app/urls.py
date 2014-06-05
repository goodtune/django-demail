from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from touchtechnology.common.sites import AccountsSite
accounts = AccountsSite()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'test_app.views.home', name='home'),
    # url(r'^test_app/', include('test_app.foo.urls')),
    url(r'^accounts/', include(accounts.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
