from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
  """!
  Clase para definir el serializer del perfil
  """

  user_id = serializers.IntegerField(write_only=True)

  class Meta:
    model = Profile
    fields = ('user_id','address','phone','gender')