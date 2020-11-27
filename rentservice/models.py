from django.db import models


class Street(models.Model):
    name = models.CharField(max_length=30, blank=False)
    street_number = models.IntegerField()
    city = models.ForeignKey(verbose_name="city", to="City", null=True, blank=False, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=51, blank=False)
    longitude = models.IntegerField()
    latitude = models.IntegerField()

    def __str__(self):
        return self.name


class Apartment(models.Model):
    price = models.IntegerField()
    area = models.IntegerField()
    rooms = models.IntegerField(default=0)
    floor = models.IntegerField(default=0)
    city = models.ForeignKey(verbose_name='city', to="City", null=True, blank=False, on_delete=models.SET_NULL)
    street = models.ForeignKey(verbose_name='street', to="Street", null=True, blank=False, on_delete=models.SET_NULL)
    free = models.BooleanField(default=True)
    width = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.area} sq.m. apartment with {self.rooms} room(s) in {self.city} for {self.price} USD {self.width} meters wide"
