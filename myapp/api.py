from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Dht11
from .serializer import Dht11serialize
from rest_framework import generics

@api_view(['GET'])
def Mylist(request):
    all_data = Dht11.objects.all()
    data = Dht11serialize(all_data,many=True).data
    return Response({'data':data})

class DhtViews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = Dht11serialize
