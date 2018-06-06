from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from corelogistics.models import Parcel
from .serializers import ParcelSerializer, ParcelPriceSerializer

# Create your views here.

class SerializedResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(SerializedResponse, self).__init__(content, **kwargs)

@csrf_exempt
def parcel_list(request):
    if request.method == 'GET':
        parcel = Parcel.objects.all()
        serializer = ParcelSerializer(parcel, many=True)
        return SerializedResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ParcelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return SerializedResponse(serializer.data, status=201)
        return SerializedResponse(serializer.errors, status=400)


@csrf_exempt
def request_detail(request, pk):
    try:
        parcel = Parcel.objects.get(track_n=pk)
    except Parcel.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = ParcelSerializer(parcel)
        return SerializedResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ParcelSerializer(parcel, data=data)
        if serializer.is_valid():
            serializer.save()
            return SerializedResponse(serializer.data)
        return SerializedResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        parcel.delete()
        return HttpResponse(status=204)

def price_request(request, pk):
    try:
        parcel = Parcel.objects.get(track_n=pk)
    except Parcel.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = ParcelPriceSerializer(parcel.price)
        return SerializedResponse(serializer.data)
    else:
        return HttpResponse(status=403)