from django.db.models.signals import post_save, post_delete,pre_save
from django.dispatch import receiver
from .models import OrderItem,Order
@receiver(post_save, sender=OrderItem)
def update_order_total_on_save(sender, instance, **kwargs):
    order:Order = instance.order
    order.calculate_total()
    order.save(update_fields=["total_sum"])


@receiver(post_delete, sender=OrderItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    order:Order = instance.order
    order.calculate_total()
    order.save(update_fields=["total_sum"])


@receiver(pre_save, sender=Order)
def update_order_status_and_quantity(sender, instance: Order, **kwargs):
    if not instance.pk:
        if instance.status == Order.CONFIRMED:
            instance.confirm_order()
    
    else:
        old_order = Order.objects.filter(pk=instance.pk).first()
        if old_order:
            if old_order.status != instance.status:
                if instance.status == Order.CONFIRMED:
                    instance.confirm_order()