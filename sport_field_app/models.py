from django.db import models


class SportField(models.Model):
    name = models.CharField(max_length=128)
    size = models.CharField(max_length=32)
    disciplines = models.ManyToManyField("SportDiscipline")
    lighting = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, default=51.79163)  # +- 90 degrees N/S
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=20.90698)  # +- 180 degrees E/W


class SportDiscipline(models.Model):
    name = models.CharField(max_length=128)


class SportFieldReservation(models.Model):
    sport_field = models.ForeignKey(SportField, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ("sport_field_id", "date",)
