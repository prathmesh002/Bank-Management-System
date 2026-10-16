from django.db import models


class accounts(models.Model):
    acc_number = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=40)
    password = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    address = models.CharField(max_length=40)
    mobile_no = models.CharField(max_length=15)

    def __str__(self):
        return self.name