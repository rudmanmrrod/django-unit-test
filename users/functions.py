from django.contrib.auth.models import User

    
def validate_email(email):
    """!
    Función que permite validar la cedula

    @date 20-04-2017
    @param cedula {str} Recibe el número de cédula
    @return Devuelve verdadero o falso
    """
    
    email = User.objects.filter(email=email)
    if email:
        return True
    else:
        return False
    
def validate_username(username):
    """!
    Función que permite validar el nombre de usuario

    @date 20-09-2017
    @param username {str} Recibe el nombre de usuario
    @return Devuelve verdadero o falso
    """
    
    usr = User.objects.filter(username=username)
    if usr:
        return True
    else:
        return False