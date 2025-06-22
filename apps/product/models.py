from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(
        "Название",
        max_length=250
    )
    description = models.TextField(
        "Описание",
    )
    price = models.IntegerField(
        "Цена",
    )
    stock_quantity = models.IntegerField(
        "Остаток"
    )
    is_active = models.BooleanField(
        "Доступен для заказа",
        default=True
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-id"]
    
    def __str__(self):
        return f"Название-{self.name}-Кол({self.stock_quantity})"