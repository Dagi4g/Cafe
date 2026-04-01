from django import forms
from django.forms import modelformset_factory
from .models import OrderItem
from django.forms import formset_factory


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['food', 'quantity', 'price']
        widgets = {
            'food': forms.HiddenInput(),
            'price': forms.HiddenInput(),
            'quantity': forms.Select(choices=[("0","Select")]+[(i,i) for i in range(1,11)]),
        }

# Formset for multiple order items

OrderItemFormSet = formset_factory(OrderItemForm, extra=0)

