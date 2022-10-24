from django.db import models


class Beer(models.Model):

    ref         = models.CharField(max_length=100, unique=True)
    name        = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, unique=True, null=True)

    def __str__(self):
        return self.name


class Bar(models.Model):
    
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Stock(models.Model):

    reference   = models.ForeignKey(Beer, on_delete=models.CASCADE)
    bar         = models.ForeignKey(Bar, on_delete=models.CASCADE)
    stock       = models.PositiveSmallIntegerField()

    class Meta:
        # set unique index for the two foreign keys together
        unique_together = ("reference", "bar")

    def __str__(self):
        return f"beer {self.reference} in bar counter {self.bar} has quantity {self.stock}"


class Orders(models.Model):

    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)

    def __str__(self):
        return f"order {self.pk} at bar {self.bar}"

    @property
    def items(self):
        return self.orderitems_set.all()

    class Meta:
        verbose_name_plural = verbose_name = "Orders"


class OrderItems(models.Model):

    order       = models.ForeignKey(Orders, on_delete=models.CASCADE)
    reference   = models.ForeignKey(Beer, on_delete=models.CASCADE)
    count       = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.order} sold {self.count} beer {self.reference}"

    class Meta:
        verbose_name_plural = verbose_name = "OrderItems"
