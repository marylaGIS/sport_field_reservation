from django.db import models


class SportField(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey("SportFieldOwner", on_delete=models.CASCADE, blank=True, null=True)
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
        unique_together = ("sport_field", "date",)


OWNERSHIP_TYPE = (
    (0, "undefined"),
    (1, "local government"),
    (2, "educational institution"),
    (3, "sport institution"),
    (4, "private"),
)


class SportFieldOwner(models.Model):
    name = models.CharField(max_length=128)
    ownership_type = models.IntegerField(choices=OWNERSHIP_TYPE, default=0)


class Message(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    subject = models.CharField(max_length=128)
    message = models.TextField()
    message_date = models.DateTimeField(auto_now_add=True)
