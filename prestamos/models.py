from random import shuffle

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

"""
Información de artículos
"""


class Category(models.Model):
    """

    """

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    """

    """

    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"

    image = models.ImageField(default='default.png')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ManyToManyField(Category, related_name='items', blank=True)

    def avalable_units(self):
        return Unit.objects.filter(item=self, available=True)

    def units_available(self, start_date, end_date):
        """
        Verifica la disponibilidad de unidades del artículo entre las fechas especificadas.
        
        :param start_date: Fecha y hora de inicio
        :param end_date: Fecha y hora de finalización
        :return: Una lista de unidades disponibles
        """
        return [unit for unit in self.units.all() if unit.is_available(start_date, end_date)]

    def __str__(self):
        return self.name


class Unit(models.Model):
    """

    """

    class Meta:
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades"
        unique_together = ('item', 'serial_number')

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='units')
    serial_number = models.CharField(max_length=255)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.item.name} - {self.serial_number}'


"""
Ordenes, Reportes y estados
"""


class OrderStatusChoices(models.TextChoices):
    """

    """

    PENDING = 'pending', _('Pendiente')
    CANCELLED = 'cancelled', _('Cancelada')
    APPROVED = 'approved', _('Aprobada')
    REJECTED = 'rejected', _('Rechazada')
    DELIVERED = 'delivered', _('Entregada')
    RETURNED = 'returned', _('Devuelta')


class Order(models.Model):
    """

    """

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Ordenes"
        ordering = ["-created_at"]

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_date = models.DateTimeField(default=timezone.now, null=False)
    return_date = models.DateTimeField(default=timezone.now, null=False)
    units = models.ManyToManyField(Unit, related_name='orders')
    status = models.CharField(max_length=10, choices=OrderStatusChoices.choices, default=OrderStatusChoices.PENDING)
    approved_by = models.ForeignKey(to=User, related_name='approved_orders', null=True, blank=True,
                                    on_delete=models.SET_NULL, default=None)

    def cancel(self):
        self.status = OrderStatusChoices.CANCELLED
        self.save()

    def aprove(self, user):
        self.status = OrderStatusChoices.APPROVED
        self.approved_by = user
        self.save()

    def add_item(self, item, quantity):
        """

        :param item:
        :param quantity:
        :return:
        """
        units = item.units_available(self.order_date, self.return_date)

        if quantity > len(units):  # Veríficar que hay suficientes unidades
            raise ValidationError("No hay suficientes unidades de '" + str(item.name) + "' diponibles")

        shuffle(units)  # revolver los elementos de la lista
        self.units.add(*(units[:quantity]))  # agregar la cantidad de unidades especificadas

    def get_report(self):
        """

        :return:
        """
        return getattr(self, 'reports', None)

    def __str__(self):
        return f'Orden {self.id} - {self.user.username}'


class Report(models.Model):
    class Meta:
        verbose_name_plural = "Reportes"

    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name='reports', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.OneToOneField(to=Order, on_delete=models.CASCADE, related_name='reports')
    details = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
