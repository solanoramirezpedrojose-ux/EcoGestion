from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models.deletion import ProtectedError
from .models import Persona
from .serializers import PersonaSerializer

@api_view(['GET','POST'])
def lista_personas(request):
    if request.method == 'GET':
        if not request.user.has_perm('personas.view_persona'):
            return Response(
                {'error','No tiene permiso para consultar personas'},
                status = status.HTTP_403_FORBIDDEN
            )
        personas = Persona.objects.all().order_by('nombre')
        serializer = PersonaSerializer(personas, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.has_perm('persona.add_persona'):
            return Response(
                {'error':'No tiene permiso para crear personas'},
                status = status.HTTP_403_FORBIDDEN
            )
        serializer = PersonaSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(
                serializer.errors,
                status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET','PUT','PATCH','DELETE'])
def detalle_persona(request, pk):
    persona = get_object_or_404(Persona, pk=pk)

    if request.method == 'GET':
        if not request.user.has_perm('personas.view_persona'):
            return Response(
                {'error':'No tiene permiso para consultar personas'},
                status = status.HTTP_403_FORBIDDEN 
            )
        serializer = PersonaSerializer(persona)
        return Response(serializer.data)
    elif request.method == 'PUT':
        if not request.user.has_perm('persona.change_persona'):
            return Response(
                {'error','No tiene permiso para modificar personas'},
                status = status.HTTP_403_FORBIDDEN
            )
        serializer = PersonaSerializer(
            persona,
            data = request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )
    elif request.method == 'PATCH':
        if not request.user.has_perm('personas.change_persona'):
            return Response(
                {'error':'No tiene permiso para modificar personas'},
                status = status.HTTP_403_FORBIDDEN
            )
        serializer = PersonaSerializer(
            persona,
            data = request.data,
            partial = True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )
    elif request.method == 'DELETE':
        if not request.user.has_perm('personas.delete_persona'):
            return Response(
                {'error':'No tiene permiso para eliminar personas'},
                status = status.HTTP_403_FORBIDDEN
            )
        try:
            persona.delete()
            return Response(
                status = status.HTTP_204_NO_CONTENT
            )
        except ProtectedError:
            return Response(
                {
                    'error':'No se puede eliminar una persona con registros relacionados'
                },
                status = status.HTTP_409_CONFLICT
            )
        