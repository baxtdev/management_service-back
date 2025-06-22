from decimal import Decimal
from django.db import models, transaction
from django.utils import timezone
from django.core.exceptions import ValidationError

class Order(models.Model):
    DRAFT = 'draft'
    CONFIRMED = 'confirmed'
    SHIPPED = 'shipped'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (DRAFT, "Черновик"),
        (CONFIRMED, "Подтвержден"),
        (SHIPPED, "Отправлен"),
        (CANCELLED, "Отменен"),
    ]

    customer = models.ForeignKey(
        "client.Client",
        verbose_name="Клиент",
        on_delete=models.CASCADE,
        related_name="orders"
    )
    date = models.DateTimeField(
        "Дата заказа",
        default=timezone.now
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default=DRAFT
    )
    total_sum = models.DecimalField(
        "Итоговая сумма",
        max_digits=12,
        decimal_places=2,
        default=0
    )

    DELIVERY_THRESHOLD = Decimal("2000")
    DELIVERY_COST = Decimal("500")  # если ниже порога
    GLOBAL_DISCOUNT_THRESHOLD = Decimal("150000")
    GLOBAL_DISCOUNT_PERCENT = Decimal("10")
    TAX_PERCENT = Decimal("12")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-date"]

    def __str__(self):
        return f"Заказ №{self.id} - {self.customer.full_name}"

    def calculate_total(self):
        subtotal = Decimal("0")
        for item in self.items.all():
            subtotal += item.get_total_price()

        if subtotal > self.GLOBAL_DISCOUNT_THRESHOLD:
            global_discount = subtotal * self.GLOBAL_DISCOUNT_PERCENT / 100
        else:
            global_discount = Decimal("0")

        subtotal_after_discount = subtotal - global_discount

        # Налоги (НДС)
        tax = subtotal_after_discount * self.TAX_PERCENT / 100

        # Доставка
        if subtotal_after_discount >= self.DELIVERY_THRESHOLD:
            delivery = Decimal("0")
        else:
            delivery = self.DELIVERY_COST

        self.total_sum = subtotal_after_discount + tax + delivery
        return self.total_sum

    @transaction.atomic
    def confirm_order(self):
        if self.status != self.DRAFT:
            raise ValidationError("Подтверждение возможно только из статуса черновика")

        for item in self.items.select_related("product"):
            if item.product.stock_quantity < item.quantity:
                raise ValidationError(
                    f"Недостаточно товара '{item.product.name}' на складе"
                )
        
        for item in self.items.select_related("product"):
            item.product.stock_quantity -= item.quantity
            item.product.save()

        self.status = self.CONFIRMED
        self.calculate_total()
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        "order.Order",
        verbose_name="Заказ",
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        "product.Product",
        verbose_name="Товар",
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(
        "Количество",
        default=1
    )
    price = models.DecimalField(
        "Цена за единицу",
        max_digits=10,
        decimal_places=2,
        default=0
    )
    discount = models.DecimalField(
        "Скидка (%)",
        max_digits=5,
        decimal_places=2,
        default=0
    )

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

    def get_total_price(self):
        if self.price is None or self.quantity is None:
            return 0
        return (self.price * self.quantity) * (1 - (self.discount or 0) / 100)
