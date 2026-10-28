from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Recoleccion, DetalleRecoleccion
from .serializers import RecoleccionSerializer, DetalleRecoleccionSerializer
from inventario.models import Material

# LISTAR Y CREAR RECOLECCIONES
@api_view(['GET','POST'])
def lista_recolecciones(request):
    if request.method == 'GET':
        if not request.user.has_perm('recolecciones.view_recoleccion'):
            return Response(
                {'error':'No tiene permiso para consultar recolecciones'},
                status = status.HTTP_403_FORBIDDEN
            )
        recolecciones = Recoleccion.objects.all()
        estado = request.GET.get('estado')
        proveedor = request.GET.get('proveedor')

        if estado:
            recolecciones = recolecciones.filter(estado = estado)
        if proveedor:
            if not proveedor.isdigit():
                return Response(
                    {'error':'El ID del proveedor no es válido.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recolecciones = recolecciones.filter(
                proveedor_id=proveedor
            )
        recolecciones = recolecciones.order_by('-fecha', '-id')

        paginador = PageNumberPagination()
        paginador.page_size = 5
        pagina = paginador.paginate_queryset(
            recolecciones, request
        )

        serializer = RecoleccionSerializer(pagina, many=True)

        return paginador.get_paginated_response(
            serializer.data
        )
    elif request.method == 'POST':
        if not request.user.has_perm('recolecciones.add_recoleccion'):
            return Response(
                {'error':'No tiene permiso para crear recolecciones'},
                status = status.HTTP_403_FORBIDDEN
            )
        serializer = RecoleccionSerializer(data = request.data)
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

# CONSULTAR, MODIFICAR Y ELIMINAR RECOLECCIONES
@api_view(['GET','PUT','PATCH','DELETE'])
def detalle_recoleccion(request, pk):
    recoleccion = get_object_or_404(Recoleccion, pk = pk)

    if request.method == 'GET':
        if not request.user.has_perm('recolecciones.view_recoleccion'):
            return Response(
                {'error','No tiene permiso para consultar recolecciones'},
                status = status.HTTP_403_FORBIDDEN
            )
        serializer = RecoleccionSerializer(recoleccion)
        return Response(serializer.data)
    elif request.method in ['PUT','PATCH']:
        if not request.user.has_perm('recolecciones.change_recoleccion'):
            return Response(
                {'error':'No tiene permiso para eliminar recolecciones'},
                status = status.HTTP_403_FORBIDDEN
            )
        if recoleccion.estado != 'PENDIENTE':
            return Response(
                {'error':'Solo se pueden modificar recolecciones pendientes.'},
                status=status.HTTP_409_CONFLICT
            )
        serializer = RecoleccionSerializer(
            recoleccion,
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
        if not request.user.has_perm('recolecciones.delete_recoleccion'):
            return Response(
                {'error':'No tiene permiso para eliminar recolecciones'},
                status = status.HTTP_403_FORBIDDEN
            )
        if recoleccion.estado != 'PENDIENTE':
            return Response(
                {'error':'No se puede eliminar una recolección finalizada.'},
                status=status.HTTP_409_CONFLICT
            )
        recoleccion.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

# CONFIRMAR RECOLECCION
@api_view(['POST'])
def confirmar_recoleccion(request, pk):
    if not request.user.has_perm('reolecciones.change_recoleccion'):
        return Response(
            {'error':'No tiene permiso para confirmar recolecciones'},
            status = status.HTTP_403_FORBIDDEN
        )
    recoleccion = get_object_or_404(Recoleccion, pk=pk)

    if recoleccion.estado != 'PENDIENTE':
        return Response(
            {'error':'La recolección ya fue recibida o cancelada.'},
            status=status.HTTP_409_CONFLICT
        )
    detalles = DetalleRecoleccion.objects.filter(
        recoleccion=recoleccion
    )
    if not detalles.exists():
        return Response(
            {'error':'La recolección no tiene materiales.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # VALIDAR LOS MATERIALES
    for detalle in detalles:
        if detalle.cantidad_kg <= 0:
            return Response(
                {'error':'La cantidad debe ser mayor a cero.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not detalle.material.activo:
            return Response(
                {'error':'El material está inactivo.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    # SUMAR LAS CANTIDADES AL INVENTARIO
    for detalle in detalles:
        material = Material.objects.get(pk=detalle.material_id)
        material.stock_kg = material.stock_kg + detalle.cantidad_kg
        material.save()

    recoleccion.estado = 'RECIBIDA'
    recoleccion.save()

    serializer = RecoleccionSerializer(recoleccion)

    return Response(serializer.data)

# CANCELAR RECOLECCION
@api_view(['POST'])
def cancelar_recoleccion(request, pk):
    if not request.user.has_perm('recolecciones.change_recoleccion'):
        return Response(
            {'error':'No tiene permiso para cancelar inscripciones'},
            status = status.HTTP_403_FORBIDDEN
        )
    recoleccion = get_object_or_404(Recoleccion, pk=pk)

    if recoleccion.estado != 'PENDIENTE':
        return Response(
            {'error':'Solo se pueden cancelar recolecciones pendientes.'},
            status=status.HTTP_409_CONFLICT
        )
    recoleccion.estado = 'CANCELADA'
    recoleccion.save()

    serializer = RecoleccionSerializer(recoleccion)

    return Response(serializer.data)

# LISTAR Y CREAR DETALLES DE RECOLECCION
@api_view(['GET','POST'])
def lista_detalles_recoleccion(request):
    if request.method == 'GET':
        if not request.user.has_perm('recolecciones.view_detallerecoleccion'):
            return Response(
                {'error':'No tiene permiso para consultar detalles'},
                status = status.HTTP_403_FORBIDDEN
            )
        detalles = DetalleRecoleccion.objects.all()
        recoleccion = request.GET.get('recoleccion')

        if recoleccion:
            if not recoleccion.isdigit():
                return Response(
                    {'error':'El ID de la recolección no es válido.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            detalles = detalles.filter(
                recoleccion_id=recoleccion
            )

        serializer = DetalleRecoleccionSerializer(
            detalles, many=True
        )

        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.has_perm('recolecciones.add_detallerecoleccion'):
            return Response(
                {'error':'No tiene permiso para agregar detaller'},
                status = status.HTTP_403_FORBIDDEN
            )
        serializer = DetalleRecoleccionSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

# CONSULTAR, MODIFICAR Y ELIMINAR DETALLES
@api_view(['GET','PUT','PATCH','DELETE'])
def detalle_material_recoleccion(request, pk):
    detalle = get_object_or_404(
        DetalleRecoleccion, pk=pk
    )

    if request.method == 'GET':
        if not request.user.has_perm('recolecciones.view_detallerecoleccion'):
            return Response(
                {'error','No tiene permiso para consultar detalles'},
                status = status.HTTP_403_FORBIDDEN
            )
        serializer = DetalleRecoleccionSerializer(detalle)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        if not request.user.has_perm('recolecciones.change_detallerecoleccion'):
            return Response(
                {'error':'No tiene permiso para modificar detaller'},
                status = status.HTTP_403_FORBIDDEN
            )
        if detalle.recoleccion.estado != 'PENDIENTE':
            return Response(
                {'error':'No se puede modificar una recolección finalizada.'},
                status=status.HTTP_409_CONFLICT
            )
        serializer = DetalleRecoleccionSerializer(
            detalle,
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
        if not request.has_perm('recolecciones.delete_detallerecoleccion'):
            return Response(
                {'error':'No tiene permiso para eliminar detaller'},
                status = status.HTTP_403_FORBIDDEN
            )
        if detalle.recoleccion.estado != 'PENDIENTE':
            return Response(
                {'error':'No se puede eliminar un detalle de una recolección finalizada.'},
                status=status.HTTP_409_CONFLICT
            )

        detalle.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )