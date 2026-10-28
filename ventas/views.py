from django.shortcuts import get_object_or_404
from django.db.models.deletion import ProtectedError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Venta, DetalleVenta
from .serializers import VentaSerializer, DetalleVentaSerializer
from inventario.models import Material

# CALCULAR EL TOTAL DE UNA VENTA
def actualizar_total_venta(venta):
    total = 0
    detalles = DetalleVenta.objects.filter(venta=venta)
    for detalle in detalles:
        total += detalle.subtotal
    venta.total = total
    venta.save()

# LISTAR Y CREAR VENTAS
@api_view(['GET', 'POST'])
def lista_ventas(request):
    if request.method == 'GET':
        if not request.user.has_perm('ventas.view_venta'):
            return Response(
                {'error':'No tiene permiso para consultar ventas.'},
            status = status.HTTP_403_FORBIDDEN
        )
        ventas = Venta.objects.all()
        estado = request.GET.get('estado')
        comprador = request.GET.get('comprador')

        if estado:
            ventas = ventas.filter(estado=estado)
        if comprador:
            if not comprador.isdigit():
                return Response(
                    {'error':'El ID del comprador no es válido.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            ventas = ventas.filter(comprador_id=comprador)
        ventas = ventas.order_by('-fecha')
        serializer = VentaSerializer(ventas, many=True)
        
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.has_perm('ventas.add_venta'):
            return Response(
                {'error':'No tiene permiso para crear ventas.'},
                status = status.HTTP_403_FORBIDDEN
            )
        serializer = VentaSerializer(data=request.data)
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

# CONSULTAR, ACTUALIZAR Y ELIMINAR UNA VENTA
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def detalle_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'GET':
        if not request.user.has_perm('ventas.view_venta'):
            return Response(
                {'error':'No tiene permiso para consultar ventas.'},
                status = status.HTTP_403_FORBIDDEN
            )
        serializer = VentaSerializer(venta)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        if not request.user.has_perm('ventas.change_venta'):
            return Response(
                {'error': 'No tiene permiso para modificar ventas.'},
                status=status.HTTP_403_FORBIDDEN
            )
        if venta.estado != 'PENDIENTE':
            return Response(
                {'error': 'Solo se pueden modificar ventas pendientes.'},
                status=status.HTTP_409_CONFLICT
            )

        serializer = VentaSerializer(
            venta,
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
        if not request.user.has_perm('ventas.delete_venta'):
            return Response(
                {'error': 'No tiene permiso para eliminar ventas.'},
                status=status.HTTP_403_FORBIDDEN
            )
        if venta.estado != 'PENDIENTE':
            return Response(
                {'error': 'No se puede eliminar una venta finalizada.'},
                status=status.HTTP_409_CONFLICT
            )

        try:
            venta.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response(
                {'error': 'La venta tiene registros relacionados.'},
                status=status.HTTP_409_CONFLICT
            )

# CONFIRMAR UNA VENTA
@api_view(['POST'])
def confirmar_venta(request, pk):
    if not request.user.has_perm('ventas.change_venta'):
        return Response(
            {'error': 'No tiene permiso para confirmar ventas.'},
            status=status.HTTP_403_FORBIDDEN
        )
    venta = get_object_or_404(Venta, pk=pk)
    if venta.estado != 'PENDIENTE':
        return Response(
            {'error': 'La venta ya fue confirmada o anulada.'},
            status=status.HTTP_409_CONFLICT
        )
    
    detalles = DetalleVenta.objects.filter(venta=venta)

    if not detalles.exists():
        return Response(
            {'error': 'La venta no tiene materiales.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # VERIFICAR LAS EXISTENCIAS
    for detalle in detalles:
        if detalle.cantidad_kg <= 0 or detalle.precio_unitario <= 0:
            return Response(
                {'error': 'La cantidad y el precio deben ser mayores a cero.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        material = detalle.material

        if not material.activo:
            return Response(
                {'error': 'El material está inactivo.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # SUMAR LAS CANTIDADES SI SE REPITE UN MATERIAL
        cantidad_total = 0
        for otro in detalles:
            if otro.material_id == detalle.material_id:
                cantidad_total += otro.cantidad_kg
        if material.stock_kg < cantidad_total:
            return Response(
                {'error': 'No hay suficiente stock de ' + material.nombre},
                status=status.HTTP_409_CONFLICT
            )
    # DESCONTAR LOS MATERIALES
    for detalle in detalles:
        material = Material.objects.get(pk=detalle.material_id)
        material.stock_kg = material.stock_kg - detalle.cantidad_kg
        material.save()
    actualizar_total_venta(venta)

    venta.estado = 'CONFIRMADA'
    venta.save()
    serializer = VentaSerializer(venta)

    return Response(serializer.data)

# ANULAR UNA VENTA
@api_view(['POST'])
def anular_venta(request, pk):
    if not request.user.has_perm('ventas.change_venta'):
        return Response(
            {'error':'No tiene permiso para anular ventas'},
            status = status.HTTP_403_FORBIDDEN
        )
    
    venta = get_object_or_404(Venta, pk=pk)
    if venta.estado != 'PENDIENTE':
        return Response(
            {'error': 'Solo se pueden anular ventas pendientes.'},
            status=status.HTTP_409_CONFLICT
        )

    venta.estado = 'ANULADA'
    venta.save()
    serializer = VentaSerializer(venta)

    return Response(serializer.data)

# LISTAR Y CREAR DETALLES DE VENTA
@api_view(['GET', 'POST'])
def lista_detalles_venta(request):
    if request.method == 'GET':
        if not request.user.has_perm('ventas.view_detalleventa'):
            return Response(
                {'error': 'No tiene permiso para consultar detalles de ventas.'},
                status=status.HTTP_403_FORBIDDEN
            )     
        detalles = DetalleVenta.objects.all()
        venta = request.GET.get('venta')

        if venta:
            if not venta.isdigit():
                return Response(
                    {'error': 'El ID de la venta no es válido.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            detalles = detalles.filter(venta_id=venta)
        
        serializer = DetalleVentaSerializer(detalles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.has_perm('ventas.add_detalleventa'):
            return Response(
                {'error': 'No tiene permiso para agregar detalles de ventas.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = DetalleVentaSerializer(data=request.data)
        if serializer.is_valid():

            cantidad = serializer.validated_data['cantidad_kg']
            precio = serializer.validated_data['precio_unitario']
            subtotal = cantidad * precio
            detalle = serializer.save(subtotal=subtotal)

            actualizar_total_venta(detalle.venta)

            return Response(
                DetalleVentaSerializer(detalle).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

# CONSULTAR, ACTUALIZAR Y ELIMINAR DETALLES
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def detalle_material_venta(request, pk):
    detalle = get_object_or_404(DetalleVenta, pk=pk)
    if request.method == 'GET':
        if not request.user.has_perm('ventas.view_detalleventa'):
            return Response(
                {'error': 'No tiene permiso para consultar detalles de ventas.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = DetalleVentaSerializer(detalle)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        if not request.user.has_perm('ventas.change_detalleventa'):
            return Response(
                {'error': 'No tiene permiso para modificar detalles de ventas.'},
                status=status.HTTP_403_FORBIDDEN
            )
        if detalle.venta.estado != 'PENDIENTE':
            return Response(
                {'error': 'No se puede modificar una venta finalizada.'},
                status=status.HTTP_409_CONFLICT
            )
        serializer = DetalleVentaSerializer(
            detalle,
            data=request.data,
            partial=(request.method == 'PATCH')
        )
        if serializer.is_valid():
            cantidad = serializer.validated_data.get(
                'cantidad_kg', detalle.cantidad_kg
            )
            precio = serializer.validated_data.get(
                'precio_unitario', detalle.precio_unitario
            )
            
            subtotal = cantidad * precio
            serializer.save(subtotal=subtotal)
            actualizar_total_venta(detalle.venta)

            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    elif request.method == 'DELETE':
        if not request.user.has_perm('ventas.delete_detalleventa'):
            return Response(
                {'error': 'No tiene permiso para eliminar detalles de ventas.'},
                status=status.HTTP_403_FORBIDDEN
            )
        if detalle.venta.estado != 'PENDIENTE':
            return Response(
                {'error': 'No se puede eliminar un detalle de una venta finalizada.'},
                status=status.HTTP_409_CONFLICT
            )
        venta = detalle.venta
        detalle.delete()

        actualizar_total_venta(venta)

        return Response(status=status.HTTP_204_NO_CONTENT)