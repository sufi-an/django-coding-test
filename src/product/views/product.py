import json
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from product.forms import ProductForm, ProductVariantPriceForm
from product.models import Product, ProductVariant, ProductVariantPrice, Variant
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.shortcuts import render,get_object_or_404, redirect

from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend

class BaseProductView(generic.View):
    form_class = ProductForm
    model = Product
    template_name = 'products/create.html'
    success_url = 'products/list.html'


class ProductList(BaseProductView, ListView):
    template_name = 'products/list.html'
    # paginate_by = 2
    p = Paginator(Product, 2)
    context_object_name = 'product_list'
    filter_flag=False
    form_class = ProductVariantPriceForm
    def get_queryset(self):
        filter_string = {}
        print(self.request.GET)
        for key in self.request.GET:
            if self.request.GET.get(key):
                if key == 'page':
                    break

                filter_string[key] = self.request.GET.get(key)
                self.filter_flag=True

        return ProductVariantPrice.objects.filter(**filter_string)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = True
        products = None
        if self.filter_flag:
            tmp_list = set([])
            for v in self.get_queryset():
                tmp_list.add(v.product)
            products = list(tmp_list)
        else:   
            products = Product.objects.all()
        
        variants = ProductVariant.objects.all()
        context['variants'] = variants
        paginator = Paginator(products, 2)  

        page_number = self.request.GET.get("page",'')
        context['products'] = paginator.get_page(page_number)
        

        context['paginator'] = paginator
        context['start_index'] = context['products'].start_index()
        context['end_index'] = context['products'].end_index()
        context['current_page'] = int(page_number)

        print(context)
        return context



@method_decorator(csrf_exempt, name='dispatch')
class CreateProductView(BaseProductView,generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context



    def post(self, request, *args, **kwargs):
        # context = self.get_context_data()
        form = self.form_class(request.POST or None)
        body = json.loads(request.body.decode())

        print(form)
        if body:
            print(body)
            # return render(request, self.success_url)
            return HttpResponseRedirect(reverse('product:list.product'))
        else:
            print('Nooooooooo')

            return render(request, self.template_name)

    # def post(self, request, *args, **kwargs):
    #     context = self.get_context_data()
        
    #     body = json.loads(request.body.decode())
    #     print(body)
        

    #     return super(generic.TemplateView, self).render_to_response(context)





