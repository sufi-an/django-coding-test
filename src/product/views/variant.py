from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView

from django.shortcuts import render,get_object_or_404, redirect

from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect


from product.forms import VariantForm
from product.models import Variant


class BaseVariantView(generic.View):
    form_class = VariantForm
    model = Variant
    template_name = 'variants/create.html'
    success_url = '/product/variants'


class VariantView(BaseVariantView, ListView):
    template_name = 'variants/list.html'
    paginate_by = 5

    def get_queryset(self):
        filter_string = {}
        print(self.request.GET)
        for key in self.request.GET:
            if self.request.GET.get(key):
                filter_string[key] = self.request.GET.get(key)
        return Variant.objects.filter(**filter_string)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = True
        context['request'] = ''
        if self.request.GET:
            context['request'] = self.request.GET['title__icontains']
        return context


class VariantCreateView(BaseVariantView, CreateView):

    def post(self, request, *args, **kwargs):
        # context = self.get_context_data()
        form = self.form_class(request.POST or None)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product:variants'))

        return render(request, self.success_url)
        
        

        


class VariantEditView(BaseVariantView, UpdateView):
    pk_url_kwarg = 'id'
