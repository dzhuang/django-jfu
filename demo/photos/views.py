from django.http import JsonResponse
from django.views.generic import (
    TemplateView, CreateView, DeleteView, ListView)
from jfu.serialize import serialize
from photos.models import Photo


class Home(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super( Home, self ).get_context_data( **kwargs )
        context['accepted_mime_types'] = ['image/*']
        return context


class ImageCreateView(CreateView):
    model = Photo
    fields = "__all__"

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JsonResponse(data)
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    
    def form_invalid(self, form):
        import json
        from django.http import HttpResponse
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')

class ImageDeleteView(DeleteView):
    model = Photo

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JsonResponse(True, safe=False)
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class ImageListView(ListView):
    model = Photo

    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.get_queryset() ]
        data = {'files': files}
        response = JsonResponse(data)
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response