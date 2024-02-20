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

        page_number = self.request.GET.get("page",1)
        context['products'] = paginator.get_page(page_number)
        

        context['paginator'] = paginator
        context['start_index'] = context['products'].start_index()
        context['end_index'] = context['products'].end_index()
        context['current_page'] = int(page_number)

        # print(context)
        return context


def handle_uploaded_file(f):

    file_path = "media/" + f.name
    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
@method_decorator(csrf_exempt, name='dispatch')
class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['operation_state']=True
        context['variants'] = list(variants.all())
        product_id = self.request.GET.get("product",'')
        if product_id:
            # product = get_object_or_404(Product,id=product_id)
            product = Product.objects.filter(id=product_id).values().first()
            print(product)
            product_variant = ProductVariant.objects.filter(product_id=product['id']).values()
            product_variant_price = ProductVariantPrice.objects.filter(product_id=product['id']).values()

            context['base_product']=product
            context['product_variant']= list(product_variant.all())
            context['list(product_variant_price']=list(product_variant_price.all())
            context['operation_state'] = 'edit'
           
        return context
    



    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body.decode())
      
            if body:
                print(body)
                product_variants = body['product_variant']
                product_variant_prices = body['product_variant_prices']

                product_instance = Product.objects.create(
                    title=body['title'],
                    sku= body['sku'], 
                    description= body['description']
                )
                product_instance.save()

                for variant in product_variants:
                    for tag in variant['tags']:
                        product_variant_instance = ProductVariant.objects.create(
                            variant_title=tag,
                            variant_id = variant['option'],
                            product=product_instance
                        )
                        product_variant_instance.save()

                
                for price in product_variant_prices:
                    # print(price['title'].split('/'))
                  
                    
                    prod_var_one, prod_var_two, prod_var_three = ProductVariant.objects.filter(product=product_instance,variant_title__in=price['title'].split('/'))
                    price_instance = ProductVariantPrice.objects.create(
                        product_variant_one = prod_var_one,
                        product_variant_two = prod_var_two,
                        product_variant_three = prod_var_three,
                        price = price['price'],
                        stock = price['stock'],
                        product = product_instance 
                    )
                    price_instance.save()
                return render(request, self.success_url)
                # return HttpResponseRedirect(reverse('product:list.product'))
        
        
        except Exception as e:
            print(e.args)
            return render(request, self.success_url)
        else:
           
            return render(request, self.template_name)

    def put(self, request,pk=None ,*args, **kwargs):

        print(request,148)


