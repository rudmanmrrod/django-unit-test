from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from .views import *
from .forms import *

"""!
  Clase para probar el registro de usuarios
"""
class RegisterUser(TestCase):
  def setUp(self):
    """!
    Método para configurar los valores iniciales de
    la prueba unitaria
    """
    self.factory = RequestFactory()

  def setup_request(self, request):
    """!
    Método para configurar la petición

    @param request Recibe la petición para configurar
    """
    # Session Middleware
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()
    # Message Middleware
    middleware = MessageMiddleware()
    middleware.process_request(request)
    request.session.save()

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
    self.setup_request(request)
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