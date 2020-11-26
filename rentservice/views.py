from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rentservice.models import Apartment, City, Street
from rentservice.serializers import ApartmentSerializer, CitySerializer, StreetSerializer, CityDetailSerializer, \
    ApartmentDetailSerializer


class CityList(APIView):
    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class CityDetail(APIView):
    def get(self, request, city_id):
        city = City.objects.filter(id=city_id).first()
        streets = Street.objects.filter(city__id=city_id).all()
        streets_list = [
            {'id': street.id, 'name': street.name, 'street_number': street.street_number} for street in streets
        ]
        response = {'city_name': city.name, 'streets_list': streets_list}
        print(response)

        serializer = CityDetailSerializer(data=response)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, city_id):
        city = City.objects.filter(id=city_id).first()
        if not city:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = StreetSerializer(data=request.data)
        if serializer.is_valid():
            print(city)
            Street.objects.create(city=city, name=serializer.data.get('name'), street_number=serializer.data.get('street_number'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class ApartmentDetail(APIView):

    def apartments_list(self, street_id):
        street_apartments = list(Apartment.objects.select_related().filter(street__id=street_id).values())
        return street_apartments

    def get(self, request, city_id):
        streets = Street.objects.filter(city__id=city_id)
        apartment_data = []
        for street in streets:
            apartment_list = Apartment.objects.filter(city__id=city_id, street__id=street.id).all()
            apartment_data.append({'street_name': street.name, 'apartments': [{'id': item.id, 'price': item.price} for item in apartment_list]})
        print(apartment_data)
        serializer = ApartmentDetailSerializer(data=apartment_data, many=True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, city_id):
        serializer = ApartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['city_id'] = city_id
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
