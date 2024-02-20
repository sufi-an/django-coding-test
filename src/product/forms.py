from django.forms import forms, ModelForm, CharField, TextInput, Textarea, BooleanField, CheckboxInput ,inlineformset_factory, BaseInlineFormSet
from product.models import Variant,Product,ProductVariant,ProductVariantPrice
from django_select2 import forms as s2forms

class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'active': CheckboxInput(attrs={'class': 'form-check-input', 'id': 'active'})
        }

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'sku': CheckboxInput(attrs={'class': 'form-control'})
        }


class VariantPriceWiget(s2forms.ModelSelect2Widget):
    search_fields = [
        "product_variant_one__variant__title__icontains",
        "product_variant_two__variant__title__icontains",
        "product_variant_three__variant__title__icontains"
    ]

class ProductVariantPriceForm(ModelForm):
    class Meta:
        model = ProductVariantPrice
        fields = '__all__'
        widgets = {
            "variant": VariantPriceWiget,
        }
