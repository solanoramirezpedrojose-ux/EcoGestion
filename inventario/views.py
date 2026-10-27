from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models.deletion import ProtectedError
from .models import Material
from .serializers import MaterialSerializers

@api_view(['GET','POST'])
def lista_material(request):
    if request.method == 'GET':
        materiales = Material.objects.all()
        categoria = request.GET.get('categoria')
        activo = request.GET.get('activo')
        buscar = request.GET.get('buscar')
        orden = request.GET.get('orden', 'nombre')
        if categoria:
            materiales = materiales.filter(categoria=categoria)
        if activo in ['true', 'false']:
            materiales = materiales.filter(activo=(activo == 'true'))
        if buscar:
            materiales = materiales.filter(nombre__icontains=buscar)

        ordenes_permitidos = [
            'nombre', '-nombre',
            'precio_venta_kg', '-precio_venta_kg'
        ]

        if orden not in ordenes_permitidos:
            orden = 'nombre'
        materiales = materiales.order_by(orden, 'id')

        paginador = PageNumberPagination()
        paginador.page_size = 5

        pagina = paginador.paginate_queryset(materiales, request)
        serializer = MaterialSerializers(pagina, many=True)

        return paginador.get_paginated_response(serializer.data)
    elif request.method == 'POST':
        serializer = MaterialSerializers(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def detalle_material(request, pk):

    material = get_object_or_404(Material, pk=pk)

    if request.method == 'GET':
        serializer = MaterialSerializers(material)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        serializer = MaterialSerializers(
            material,
            data=request.data,
            partial=(request.method == 'PATCH')
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':
        try:
            material.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        except ProtectedError:
            return Response(
                {
                    'error': 'No se puede eliminar un material con registros relacionados.'
                },
                status=status.HTTP_409_CONFLICT
            )