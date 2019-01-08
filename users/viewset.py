from rest_framework import  viewsets
from .serializers import *
from .models import *

class ProfileViewSet(viewsets.ModelViewSet):
  """!
    Clase para realizar el api del perfil
  """
  queryset = Profile.objects.all()
  serializer_class = ProfileSerializer