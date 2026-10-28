from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Pago
from .serializers import PagoSerializer

# LISTAR Y CREAR PAGOS
@api_view(['GET','POST'])
def lista_pagos(request):
    if request.method == 'GET':
        if not request.user.has_perm('pagos.view_pago'):
            return Response(
                {'error': 'No tiene permiso para consultar pagos.'},
                status=status.HTTP_403_FORBIDDEN
            )
        pagos = Pago.objects.all()
        venta = request.GET.get('venta')
        metodo_pago = request.GET.get('metodo_pago')

        if venta:
            if not venta.isdigit():
                return Response(
                    {'error': 'El ID de la venta no es válido.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            pagos = pagos.filter(venta_id=venta)
        if metodo_pago:
            pagos = pagos.filter(metodo_pago=metodo_pago)
        pagos = pagos.order_by('-fecha_pago')

        serializer = PagoSerializer(pagos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.has_perm('pagos.add_pago'):
            return Response(
                {'error': 'No tiene permiso para registrar pagos.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = PagoSerializer(data=request.data)
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

# CONSULTAR, MODIFICAR Y ELIMINAR PAGOS
@api_view(['GET','PUT','PATCH','DELETE'])
def detalle_pago(request, pk):
    pago = get_object_or_404(Pago, pk = pk)

    if request.method == 'GET':
        if not request.user.has_perm('pagos.view_pago'):
            return Response(
                {'error': 'No tiene permiso para consultar pagos.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = PagoSerializer(pago)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        if not request.user.has_perm('pagos.change_pago'):
            return Response(
                {'error': 'No tiene permiso para modificar pagos.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = PagoSerializer(
            pago,
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
        if not request.user.has_perm('pagos.delete_pago'):
            return Response(
                {'error': 'No tiene permiso para eliminar pagos.'},
                status=status.HTTP_403_FORBIDDEN
            )
        pago.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )