from rest_framework.decorators import api_view
from rest_framework.response import Response

# Consultamos la información y permisos del usuario autenticado
@api_view(['GET'])
def usuario_actual(request):
    # Obtenemos el usuario que inició sesión
    usuario = request.user

    # Consultamos sus grupos y permisos asignados en Django
    grupos = list(usuario.groups.values_list('name', flat=True))
    permisos = list(usuario.get_all_permissions())

    return Response({
        'username': usuario.username,
        'grupos': grupos,
        'permisos': permisos
    })