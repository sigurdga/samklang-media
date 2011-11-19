from django.conf.urls.defaults import *
from samklang_media.views import *

urlpatterns = patterns('',
    #(r'^images.json$', images_json, {}),
    #(r'^image/new$', ImageCreateView.as_view(), {}, 'media-new-image'),
    #(r'^n/$', DocumentCreateView.as_view(), {}, 'media-new'),
    url(r'^n/$', upload_document, name="media-file-new"),
    url(r'^m/$', manage_documents, name="media-file-manage"),
    url(r'^v/(?P<pk>\d+)/$', DocumentDetailView.as_view(), name="media-file-detail"),
    (r'^e/(?P<pk>\d+)/$', DocumentUpdateView.as_view(), {}),
    url(r'^d/$', DocumentListView.as_view(queryset=Document.objects.filter(show=False)), name="media-file-unpublished"),
    url(r'^$', DocumentListView.as_view(queryset=Document.objects.filter(show=True)), name="media-file-list"),
    #(r'^image/delete/(?P<pk>\d+)$', ImageDeleteView.as_view(), {}, 'media-delete-image'),
)
