from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Client(models.Model):
    full_name = models.CharField(
        "ФИО"
    )
    email = models.EmailField(
        "Почта",
        unique=True
    )
    company_name = models.CharField(
        "Название компании",
        max_length=250,
        blank=True,
        null=True
    )
    phone = PhoneNumberField(
        "Телефон номер"
    )
    created_at = models.DateTimeField(
        "Дата регистрации",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["-id"]

    def __str__(self):
        return self.email
