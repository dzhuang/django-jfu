import os
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.http import require_POST
from jfu.http import upload_receive, UploadResponse, JFUResponse
from photos.models import Photo

class Home( generic.TemplateView ):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super( Home, self ).get_context_data( **kwargs )
        context['accepted_mime_types'] = ['image/*']
        return context

#@require_POST
#def upload( request ):
#    file = upload_receive( request )
#
#    instance = Photo( file = file )
#    instance.save()
#
#    basename = os.path.basename( instance.file.path )
#    
#    file_dict = {
#        'name' : basename,
#        'size' : file.size,
#
#        'url': settings.MEDIA_URL + basename,
#        'thumbnailUrl': settings.MEDIA_URL + basename,
#
#        'deleteUrl': reverse('jfu_delete', kwargs = { 'pk': instance.pk }),
#        'deleteType': 'POST',
#    }
#
#    return UploadResponse( request, file_dict )
#
#@require_POST
#def upload_delete( request, pk ):
#    success = True
#    try:
#        instance = Photo.objects.get( pk = pk )
#        os.unlink( instance.file.path )
#        instance.delete()
#    except Photo.DoesNotExist:
#        success = False
#
#    return JFUResponse( request, success )


#====================================================================

import json

from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, ListView
from jfu.response import JSONResponse, response_mimetype
from jfu.serialize import serialize


class ImageCreateView(CreateView):
    model = Photo
    fields = "__all__"

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        print response
        return response
    
#    def get_context_data(self, **kwargs):
#        context = super(ImageCreateView, self).get_context_data(**kwargs)
#        
#        from django.core.urlresolvers import reverse
#        #context['upload_handler_url'] = self.info_sended
#        context['upload_handler_url'] = reverse(
#            'jfu_upload', args = args, kwargs = kwargs
#        )
#        return context

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')

class ImageDeleteView(DeleteView):
    model = Photo

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class ImageListView(ListView):
    model = Photo

    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.get_queryset() ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response