from django.db import models

# Create your models here.

class Report(models.Model):
    start_date = models.DateField(
        "Начальная дата"
    )
    end_date = models.DateField(
        "Конечная дата"
    )
    file = models.FileField(
        "PDF отчет",
        upload_to="reports/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Отчет с {self.start_date} по {self.end_date}"
