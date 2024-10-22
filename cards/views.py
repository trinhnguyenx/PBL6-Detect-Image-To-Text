from rest_framework import viewsets
from rest_framework.decorators import action

from .serializer import CCCDCardSerializer
from .models import CCCDCard

# Create your views here.

class CardViewSet(viewsets.ModelViewSet):
    queryset = CCCDCard.objects.all()
    serializer_class = CCCDCardSerializer

    @action(detail=False, methods=['post'], url_path='callback')
    def callback(self, request):
        pass
