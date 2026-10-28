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
        if not request.user.has_perm('inventario.view_material'):
            return Response(
                {'error':'No tiene permiso para consultar materiales'},
                status = status.HTTP_403_FORBIDDEN
            )
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
        if not request.user.has_perm('inventario.add_material'):
            return Response(
                {'error':'No tiene permiso para crear materiales'},
                status = status.HTTP_403_FORBIDDEN
            )
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
        if not request.user.has_perm('inventario.view_material'):
            return Response(
                {'error':'No tiene permiso para consultar materiales'},
                status = status.HTTP_403_FORBIDDEN
            )
        serializer = MaterialSerializers(material)
        return Response(serializer.data)
    elif request.method in ['PUT','PATCH']:
        if not request.user.has_perm('inventario.change_material'):
            return Response(
                {'error':'No tiene permiso para modificar materiales'},
                status = status.HTTP_403_FORBIDDEN
            )
        serializer = MaterialSerializers(
            material,
            data = request.data,
            partial = (request.method == 'PATCH')
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':
        if not request.user.has_perm('inventario.delete_material'):
            return Response(
                {'error':'No tiene permiso para eliminar materiales'},
                status = status.HTTP_403_FORBIDDEN
            )
        try:
            material.delete()
            return Response(
                status = status.HTTP_204_NO_CONTENT
            )
        except ProtectedError:
            return Response(
                {
                    'error':'No se puede eliminar un material con registros relacionados.'
                },
                status = status.HTTP_409_CONFLICT
            )