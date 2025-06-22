from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile

from .models import Report
from .utils import generate_sales_report  # функция генерации PDF

from apps.order.models import Order, OrderItem

from django.db.models import Sum
from django.utils.timezone import make_aware
import datetime


@receiver(post_save, sender=Report)
def generate_report_pdf(sender, instance, created, **kwargs):
    if not created or instance.file:
        return  

    start_date = instance.start_date
    end_date = instance.end_date

    start_dt = make_aware(datetime.datetime.combine(start_date, datetime.time.min))
    end_dt = make_aware(datetime.datetime.combine(end_date, datetime.time.max))

    orders = Order.objects.filter(date__range=(start_dt, end_dt), status='confirmed')
    total_revenue = orders.aggregate(total=Sum("total_sum"))["total"] or 0
    total_orders = orders.count()

    top_clients = (
        orders.values("customer__full_name")
        .annotate(total=Sum("total_sum"))
        .order_by("-total")[:5]
    )

    items = OrderItem.objects.filter(order__in=orders)
    top_product_data = (
        items.values("product__name")
        .annotate(total_quantity=Sum("quantity"))
        .order_by("-total_quantity")
        .first()
    )

    top_product = {
        "name": top_product_data["product__name"] if top_product_data else "-",
        "total_quantity": top_product_data["total_quantity"] if top_product_data else 0
    }

    orders_data = orders.values("date", "customer__full_name", "total_sum", "status")

    context = {
        "start_date": start_date,
        "end_date": end_date,
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "top_clients": top_clients,
        "top_product": top_product,
        "orders": [
            {
                "date": o["date"].strftime("%Y-%m-%d"),
                "customer": o["customer__full_name"],
                "total_sum": o["total_sum"],
                "status": o["status"],
            }
            for o in orders_data
        ]
    }

    pdf_file = generate_sales_report(context)

    filename = f"sales_report_{start_date}_{end_date}.pdf"
    instance.file.save(filename, ContentFile(pdf_file.getvalue()))
