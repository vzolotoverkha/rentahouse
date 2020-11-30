from django.http import Http404
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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class CityDetail(APIView):

    def get_city_object(self, city_id):
        try:
            return City.objects.get(id=city_id)
        except City.DoesNotExist:
            raise Http404

    def get(self, request, city_id):
        city = self.get_city_object(city_id)

        streets = Street.objects.filter(city__id=city_id).all()
        response = {'city_name': city.name, 'streets_list': streets}
        serializer = CityDetailSerializer(response)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, city_id):
        city = self.get_city_object(city_id)

        serializer = StreetSerializer(data=request.data)
        if serializer.is_valid():
            Street.objects.create(city=city, **serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class ApartmentDetail(APIView):

    def get(self, request, city_id):
        streets = Street.objects.filter(city__id=city_id).all()
        apartment_data = []
        for street in streets:
            # apartment_list = Apartment.objects.filter(city__id=city_id, street__id=street.id).all()
            # apt_details = [{'id': item.id, 'price': item.price} for item in apartment_list]
            current_apartment = street.apartment_set.all()
            if not current_apartment:
                break
            apartment_data.append({'street_name': street.name, 'apartments': current_apartment})

        serializer = ApartmentDetailSerializer(apartment_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, city_id):
        city = City.objects.filter(id=city_id).first()
        street = request.data.get('street')

        if not street or not city:
            return Response({'error': 'forgot required fields'}, status=status.HTTP_400_BAD_REQUEST)

        street_obj = Street.objects.filter(name=street, city__id=city_id).first()

        serializer = ApartmentSerializer(data=request.data)
        if serializer.is_valid():
            Apartment.objects.create(city=city, street=street_obj, **serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApartmentFilter(APIView):
    def get(self, request):
        all_apts = Apartment.objects.all()
        price = request.query_params.get('price')
        width = request.query_params.get('width')

        if price is not None and width is not None:
            filtered = all_apts.filter(price__gt=price, width__gt=width)
            serializer = ApartmentSerializer(filtered, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
