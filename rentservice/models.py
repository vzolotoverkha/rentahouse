from django.db import models


class Street(models.Model):
    name = models.CharField(max_length=30)
    street_number = models.IntegerField(blank=True, null=True)
    city = models.ForeignKey(verbose_name="city", to="City", null=True, blank=False, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=51)
    longitude = models.IntegerField(blank=True, null=True)
    latitude = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Apartment(models.Model):
    price = models.IntegerField(blank=True, null=True)
    area = models.IntegerField(blank=True, null=True)
    rooms = models.IntegerField(blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    city = models.ForeignKey(verbose_name='city', to="City", null=True, blank=False, on_delete=models.SET_NULL)
    street = models.ForeignKey(verbose_name='street', to="Street", null=True, blank=False, on_delete=models.SET_NULL)
    free = models.BooleanField(default=True)
    width = models.IntegerField(blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.area} sq.m. apartment with {self.rooms} room(s) in {self.city} for {self.price} USD {self.width} meters wide"
