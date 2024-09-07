# views.py

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .forms import OrderForm, AuthorizeForm, OrderItemFormSet, ReporteForm
from .models import Order, Report, Item, Category, OrderStatusChoices


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "settings.html"


class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'report_list.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user, 
            order_date__gt=timezone.now(), 
            status__in=[OrderStatusChoices.PENDING, OrderStatusChoices.APPROVED]
        )
        

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user,
            order_date__gt=timezone.now(),
            status__in=[OrderStatusChoices.DELIVERED],
        )


class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReporteForm
    template_name = 'report_create.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        form.instance.user = self.request.user

        pk = self.kwargs.get('pk')  # pk de la orden en la url
        form.instance.order = get_object_or_404(Order, pk=pk)

        return super().form_valid(form)


class OrderAuthorize(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = AuthorizeForm
    template_name = 'order_authorize.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        form.instance.approved_by = self.request.user
        return super().form_valid(form)


class OrderCreateView(LoginRequiredMixin, View):
    select_item_template = 'order_form.html'
    change_date_template  = 'order_confirm.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.select_item_template, {
            'order_form': OrderForm(),
            'item_formset': OrderItemFormSet(),
            'items': Item.objects.all(),
            'categories': Category.objects.all()
        })
    

    def post(self, request, *args, **kwargs):
        order_form = OrderForm(request.POST)
        item_formset = OrderItemFormSet(request.POST)
        order = None
        
        if order_form.is_valid() and item_formset.is_valid():
            try:
                # hacer la orden 
                order = self.transaction_order(request)
                
            except Exception as e:
                # hacer que el usuario seleccione otra fecha si no esta disponible
                messages.error(request, e)
                return render(request, self.change_date_template, {
                    'item_formset': item_formset,
                    'order_form': order_form
                }) 
                
            else:
                # redirigir a la pagina de detalles de la orden
                messages.success(request, "La orden se ha creado exitosamente.")
                return redirect('order_detail', order.pk)
            
        # hacer que el usuario seleccione otra fecha 
        return render(request, self.change_date_template, {
            'item_formset': item_formset,
            'order_form': order_form
        }) 
                    
                    
    def transaction_order(self, request) -> Order:
        order_form = OrderForm(request.POST)
        item_formset = OrderItemFormSet(request.POST)
        
        with transaction.atomic():
            # agregar unidades a la orden
            order_form.instance.user = self.request.user
            order = order_form.save()

            for item_form in item_formset:
                item = item_form.cleaned_data['item']
                quantity = item_form.cleaned_data['quantity']

                if quantity < 0:
                    # si solicito 0 unidades del articulo ignorar
                    continue

                order.add_item(item, quantity)

            if order.units.count() <= 0:
                raise ValueError("La orden no tiene unidades")
        
        return order
                    

class OrderHistoryListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_history_list.html'
    context_object_name = 'orders'

    # agregar esto a una configuracion del sistema
    paginate_by = 100

    def get_queryset(self):
        # ordenes del usuario que ya hayan pasado
        return Order.objects.filter(
            user=self.request.user, 
            order_date__lt=timezone.now()
        )


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
