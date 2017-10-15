from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.conf import settings
from blog import views as blog_views
from blog import feeds
from feedstats.utils import count_subscribers
import os

FAVICON = open(os.path.join(settings.BASE_DIR, 'static/favicon.ico')).read()


def static_redirect(request):
    return HttpResponsePermanentRedirect(
        'http://static.simonwillison.net%s' % request.get_full_path()
    )

STAGING_ROBOTS_TXT = '''
User-agent: Twitterbot
Disallow:

User-agent: *
Disallow: /
'''

PRODUCTION_ROBOTS_TXT = '''
User-agent: *
Disallow: /admin/

Sitemap: https://simonwillison.net/sitemap.xml
'''


def robots_txt(request):
    if settings.STAGING:
        txt = STAGING_ROBOTS_TXT
    else:
        txt = PRODUCTION_ROBOTS_TXT
    return HttpResponse(txt, content_type='text/plain')


def favicon_ico(request):
    return HttpResponse(FAVICON, content_type='image/x-icon')


urlpatterns = [
    url(r'^$', blog_views.index),
    url(r'^(\d{4})/$', blog_views.archive_year),
    url(r'^(\d{4})/(\w{3})/$', blog_views.archive_month),
    url(r'^(\d{4})/(\w{3})/(\d{1,2})/$', blog_views.archive_day),
    url(r'^(\d{4})/(\w{3})/(\d{1,2})/([\-\w]+)/$', blog_views.archive_item),

    # Ancient URL pattern still getting hits
    url(r'^/?archive/(\d{4})/(\d{2})/(\d{2})/$', blog_views.archive_day_redirect),
    url(r'^/?archive/(\d{4})/(\d{2})/(\d{2})/([\-\w]+)/?$', blog_views.archive_item_redirect),

    url(r'^robots\.txt$', robots_txt),
    url(r'^favicon\.ico$', favicon_ico),

    url(r'^search/$', blog_views.search),
    url(r'^tags/$', blog_views.tag_index),
    url(r'^tags/(.*?)/$', blog_views.archive_tag),

    url(r'^atom/entries/$', count_subscribers(feeds.Entries().__call__)),
    url(r'^atom/links/$', count_subscribers(feeds.Blogmarks().__call__)),
    url(r'^atom/everything/$', count_subscribers(feeds.Everything().__call__)),

    url(r'^sitemap\.xml$', feeds.sitemap),

    url(r'^tools/$', blog_views.tools),
    url(r'^tools/search-tags/$', blog_views.tools_search_tags),

    url(r'^write/$', blog_views.write),
    #  (r'^about/$', blog_views.about),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/', static_redirect),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
