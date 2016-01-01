from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from photos.views import Home, ImageCreateView, ImageDeleteView, ImageListView

urlpatterns = patterns('',
    url( r'^$', Home.as_view(), name = 'home' ),
)

urlpatterns += [
    url(r'^image/upload/', ImageCreateView.as_view(), name = 'jfu_upload'),
    url(r'^image/delete/(?P<pk>\d+)$', ImageDeleteView.as_view(), name='upload-delete'),
    url(r'^image/view/$', ImageListView.as_view(), name='upload-view'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
