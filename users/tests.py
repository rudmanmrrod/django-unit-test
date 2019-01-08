from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from rest_framework.test import APIClient
from .models import *
from .forms import *
from .functions import setup_request
from .views import *

class RegisterUserTest(TestCase):
  """!
    Clase para probar el registro de usuarios
  """

  def setUp(self):
    """!
    Método para configurar los valores iniciales de
    la prueba unitaria
    """
    self.factory = RequestFactory()

  def test_get(self):
    """!
    Método para probar las peticiones por get
    """
    request = self.factory.get('/register')
    response = RegisterView.as_view()(request)
    self.assertEqual(response.status_code, 200)

  def test_post(self):
    """!
    Método para probar la vista por post,
    en este caso registrar un usuario
    """
    user = User.objects.count()
    request = self.factory.post("/register", 
      {'email': "test@mail.com", 'username': "test", 'first_name': "test",
      "last_name":"user","password1": "prueba123", "password2": "prueba123"}) 
    setup_request(request)
    response = RegisterView.as_view()(request)
    self.assertEqual(response.status_code, 302)
    self.assertEqual(User.objects.count(), user+1)

  def test_valid_form(self):
    """!
    Método para probar si el formulario es válido
    """
    form = UserRegisterForm(data = {
      'username': "test",
      'email': "test@mail.com",
      'password1': "prueba123",
      'password2': "prueba123",
      'first_name': "test",
      'last_name': "user"
    })
    self.assertTrue(form.is_valid())

  def test_invalid_form(self):
    """!
    Método para probar si el formulario es inválido
    """
    form = UserRegisterForm(data = {
      'username': "test",
      'email': "test@mail.com",
      'password1': "123",
      'password2': "123",
      'first_name': "test",
      'last_name': "user"
    })
    self.assertFalse(form.is_valid())

class LoginTest(TestCase):
  """!
    Clase para probar el login
  """

  def setUp(self):
    """!
    Método para configurar los valores iniciales de
    la prueba unitaria
    """
    self.factory = RequestFactory()
    self.user = User.objects.create_user(
      username='testuser', email='test@mail.com', password='prueba123')

  def test_get(self):
    """!
    Método para probar las peticiones por get
    """
    request = self.factory.get('/login')
    response = LoginView.as_view()(request)
    self.assertEqual(response.status_code, 200)

  def test_post(self):
    """!
    Método para probar la vista por post,
    en este caso registrar un usuario
    """
    request = self.factory.post("/login", 
      {'usuario': "test", "contrasena": "prueba1234",}) 
    setup_request(request)
    response = LoginView.as_view()(request)
    self.assertEqual(response.status_code, 200)

class ChangePasswordTest(TestCase):
  """!
    Clase para probar el cambio de contraseña
  """

  def setUp(self):
    """!
    Método para configurar los valores iniciales de
    la prueba unitaria
    """
    self.factory = RequestFactory()
    self.username = 'testuser'
    self.old_password = 'prueba123'
    self.new_password = '123prueba'
    self.user = User.objects.create_user(
      username=self.username, email='test@mail.com', password=self.old_password)

  def test_change_password(self):
    """!
    Método para probar el cambio de contraseña
    """
    request = self.factory.post("/account/change-pass/", 
      {'old_password': self.old_password, 'new_password1': self.new_password, 
      'new_password2': self.new_password})
    request.user = self.user
    response = ChangePasswordView.as_view()(request)
    self.assertEqual(response.status_code, 302)
    self.assertIsNotNone(authenticate(username='testuser', password=self.new_password))

class ProfileTest(TestCase):
  """!
    Clase para probar el perfil
  """

  def setUp(self):
    """!
    Método para configurar los valores iniciales de
    la prueba unitaria
    """
    self.factory = RequestFactory()
    self.user = User.objects.create_user(
      username='testuser', email='test@mail.com', password='prueba123')

  def test_model(self):
    """!
    Método para probar el modelo del perfil
    """
    profile = Profile()
    profile.address='dirección de prueba'
    profile.phone='+1 12345687'
    profile.gender='M'
    profile.user=self.user
    profile.save()
    self.assertEqual(profile.pk,1)

  def test_list_view(self):
    """!
    Método para probar el listado de perfiles
    """
    request = self.factory.get("/profile") 
    request.user = self.user
    #setup_request(request)
    response = ListProfileView.as_view()(request)
    self.assertEqual(response.status_code, 200)

  def test_create_view(self):
    """!
    Método para probar la creación de perfiles
    """
    profile = Profile.objects.count()
    request = self.factory.post("/profile/create", 
      {'address': "dirección de prueba",
       "phone": "+58 123456",
       "gender":"F"}) 
    request.user = self.user
    response = CreateProfileView.as_view()(request)
    self.assertEqual(response.status_code, 302)
    self.assertEqual(Profile.objects.count(), profile+1)

class ProfileRestTest(TestCase):
  """!
    Clase para probar el perfil por servicios rest
  """

  def setUp(self):
    """!
    Método para configurar los valores iniciales de
    la prueba unitaria
    """
    self.client = APIClient()
    self.user = User.objects.create_user(
      username='testuser', email='test@mail.com', password='prueba123')
    self.profile = Profile.objects.create(
      address = "dirección de prueba",
      phone = "+58 123456",
      gender = "M",
      user = self.user
    )

  def test_list(self):
    """!
    Método para probar el listado de perfiles
    """
    response = self.client.get('/api/profile/')
    self.assertEqual(response.status_code,200)

  def test_create(self):
    """!
    Método para probar el creado de un perfil
    """
    profile = Profile.objects.count()
    response = self.client.post('/api/profile/',
      {'address':'otra dirección','phone':'+1 234454',
      'gender':'M','user_id':1},format="json")
    self.assertEqual(response.status_code,201)
    self.assertEqual(Profile.objects.count(),profile + 1)
