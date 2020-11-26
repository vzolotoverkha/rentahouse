from rest_framework import serializers
from rentservice.models import Apartment, City, Street


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            'id', 'name', 'longitude', 'latitude'
        ]


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = [
            'id', 'name', 'street_number', 'city'
        ]


class ApartmentSerializer(serializers.ModelSerializer):
    street = StreetSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Apartment
        fields = [
            'id', 'price', 'area', 'rooms', 'floor', 'street', 'city', 'free', 'width', 'length', 'added'
        ]


class StreetDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    street_number = serializers.IntegerField()


class CityDetailSerializer(serializers.Serializer):
    city_name = serializers.CharField(max_length=25)
    streets_list = StreetDetailSerializer(many=True)


class AptSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    price = serializers.IntegerField()


class ApartmentDetailSerializer(serializers.Serializer):
    street_name = serializers.CharField(max_length=30)
    apartments = AptSerializer(many=True)
