from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms.models import modelformset_factory
from django.db.models.query_utils import Q

from samklang_media.models import Document
from samklang_media.forms import *

from django.shortcuts import render_to_response
from django.template import RequestContext

import os
from taggit.models import Tag, TaggedItem
import magic

from datetime import datetime, timedelta
from django.conf import settings

#def images_json(request):
    #"""Return json data of images"""
    #images = Image.objects.all()
    #data = [{'id': img.id, 'url': img.file.url, 'filename': img.filename} for img in images]
    #return JSONResponse(data)

#class ImageListView(ListView):
    #model = Image
#
    #def get_context_data(self, **kwargs):
        #popup = self.request.GET.get('popup', False)
        #context = super(ImageListView, self).get_context_data(**kwargs)
        #context['popup'] = popup
        #return context

def upload_file(request):
    form = UploadForm()
    return render_to_response('samklang_media/document_new.html', {
        'form': form,
        }, context_instance=RequestContext(request))

class ImageCreateView(CreateView):
    model = Document
    template_name = 'samklang_media/image_new.html'
    form_class = ImageForm

    def form_valid(self, form):
        mime = magic.Magic(mime=True)
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.content_type = mime.from_buffer(self.object.file.read(128))
        self.object.content_category = 1 # hardcode to "image"
        if hasattr(self.request, 'site'):
            self.object.site = self.request.site
        else:
            self.object.site = Site.objects.get(pk=1)
        self.object.save()
        return HttpResponseRedirect(reverse('media-image-list'))


class DocumentCreateView(CreateView):
    model = Document
    template_name = 'samklang_media/document_new.html'
    form_class = UploadForm

    def form_valid(self, form):
        if self.request.FILES:
            mime = magic.Magic(mime=True)
            for f in self.request.FILES.getlist('file'):
                fobj = Document()
                fobj.file = f
                fobj.filename = f.name
                fobj.content_type = mime.from_buffer(f.file.read(128))
                fobj.content_category = 0 # hardcode to "generic uncategorized document"
                if hasattr(self.request, 'site'):
                    fobj.site = self.request.site
                else:
                    fobj.site = Site.objects.get(pk=1)
                fobj.user = self.request.user
                fobj.save()
            return JSONResponse({})


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DocumentCreateView, self).dispatch(*args, **kwargs)




def upload_document(request):
    if request.method == "POST" and request.FILES and request.user.is_authenticated():
        mime = magic.Magic(mime=True)
        for f in request.FILES.getlist('file'):
            #filepath = os.path.join(settings.MEDIA_ROOT, 'uploads', f.name)
            #destination = open(filepath, 'wb+')
            #for chunk in f.chunks():
                #destination.write(chunk)
            #destination.close()
            fobj = Document()
            fobj.file = f
            fobj.filename = f.name
            fobj.content_type = mime.from_buffer(f.file.read(128))
            fobj.content_category = 1 # hardcode to "document"
            fobj.site = Site.objects.get(pk=1)
            fobj.user = request.user
            fobj.save()
        return JSONResponse({})
    else:
        form = UploadForm()
        return render_to_response('samklang_media/document_new.html', {
            'form': form,
            }, context_instance=RequestContext(request))

def manage_documents(request):
    DocumentFormset = modelformset_factory(Document, fields=("filename", "tags", "show", "group"), extra=0)
    queryset = Document.objects.filter(user=request.user, submit_date__gt=datetime.now()-timedelta(hours=1), show=False)
    if request.method == "POST":
        formset = DocumentFormset(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('media-file-list'))
    else:
        formset = DocumentFormset(queryset=queryset)
    return render_to_response("samklang_media/manage_documents.html", {
        "formset": formset,
	}, context_instance=RequestContext(request))

class DocumentListView(ListView):
    model = Document

    def get_queryset(self):
        queryset = super(DocumentListView, self).get_queryset().filter(Q(group=None) | Q(group__user=self.request.user)).filter(show=True)
        tag_url = self.kwargs.get("tags", "")
        if tag_url:
            tag_list = tag_url.split("/")
            return queryset.filter(tags__name__in=tag_list).distinct()
        else:
            return queryset

class DocumentDetailView(DetailView):
    model = Document

    def get_queryset(self):
        return super(DocumentDetailView, self).get_queryset().filter(Q(group=None) | Q(group__user=self.request.user)).filter(show=True)


class DocumentUpdateView(UpdateView):
    model = Document
    form_class = DocumentForm

    def get_queryset(self):
        return super(DocumentUpdateView, self).get_queryset().filter(Q(group=None) | Q(group__user=self.request.user)).filter(show=True)


class DocumentOldCreateView(CreateView):
    model = Document
    form_class = UploadForm
    template_name = "samklang_media/document_new.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.filename = self.request.FILES['file'].name
        self.object.user = self.request.user
        if hasattr(self.request, 'site'):
            self.object.site = self.request.site
        else:
            self.object.site = Site.objects.get(pk=1)
        self.object.save()
        return JSONResponse({})
        #return HttpResponseRedirect("/")#self.object.get_absolute_url())

    def form_invalid(self, form):
        print "FEIL"
        return JSONResponse({})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DocumentCreateView, self).dispatch(*args, **kwargs)


#class ImageCreateView(CreateView):
    #model = Image
    #form_class = SimpleImageForm
#
    #def form_valid(self, form):
        #self.object = form.save(commit=False)
        #self.object.filename = self.request.FILES['file'].name
        #self.object.user = self.request.user
        #if hasattr(self.request, 'site'):
            #self.object.site = self.request.site
        #else:
            #self.object.site = Site.objects.get(pk=1)
        #self.object.save()
#
        #filename = self.object.filename
        #object_url = self.object.file.url
        #delete_url = reverse('media-delete-image', args=[self.object.id])
        #data = [{'name': filename, 'url': object_url, 'thumbnail_url': object_url, 'delete_url': delete_url, 'delete_type': "DELETE"}]
        #return JSONResponse(data)
#
    #@method_decorator(login_required)
    #def dispatch(self, *args, **kwargs):
        #return super(ImageCreateView, self).dispatch(*args, **kwargs)


#class ImageDeleteView(DeleteView):
    #model = Image
#
    #def delete(self, request, *args, **kwargs):
        #self.object = self.get_object()
        #self.object.is_removed = True
        #self.object.save()
        #return JSONResponse(True)

class JSONResponse(HttpResponse):
    """JSON response class. This does not help browsers not liking application/json."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)
