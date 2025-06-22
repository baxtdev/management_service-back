from django.http import FileResponse
from django.utils.dateparse import parse_date
from django.db.models import Sum
from django.utils.timezone import make_aware

from rest_framework.decorators import action
from rest_framework.response import Response

from datetime import datetime, time

from apps.order.models import Order, OrderItem
from .utils import generate_sales_report

class ReportService:
    @action(detail=False, methods=["get"], url_path="sales")
    def sales_report(self, request):
        start = request.GET.get("start")
        end = request.GET.get("end")

        if not start or not end:
            return Response({"detail": "start and end required"}, status=400)

        start_date = parse_date(start)
        end_date = parse_date(end)
        start_date = make_aware(datetime.combine(parse_date(start), time.min))
        end_date = make_aware(datetime.combine(parse_date(end), time.max))

        orders = Order.objects.filter(date__range=(start_date, end_date), status='confirmed')
        print("Orders",orders)
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
        return FileResponse(pdf_file, as_attachment=True, filename="sales_report.pdf")
