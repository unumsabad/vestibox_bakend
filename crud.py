from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas

# Cliente CRUD
def get_cliente(db: Session, cliente_id: int):
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

def get_cliente_by_email(db: Session, email: str):
    return db.query(models.Cliente).filter(models.Cliente.email == email).first()

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def update_cliente(db: Session, cliente_id: int, cliente: schemas.ClienteCreate):
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        for key, value in cliente.dict().items():
            setattr(db_cliente, key, value)
        db.commit()
        db.refresh(db_cliente)
    return db_cliente

def delete_cliente(db: Session, cliente_id: int):
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
        return True
    return False

# Producto CRUD
def get_producto(db: Session, producto_id: int):
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Producto).offset(skip).limit(limit).all()

def create_producto(db: Session, producto: schemas.ProductoCreate):
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(db: Session, producto_id: int, producto: schemas.ProductoCreate):
    db_producto = get_producto(db, producto_id)
    if db_producto:
        for key, value in producto.dict().items():
            setattr(db_producto, key, value)
        db.commit()
        db.refresh(db_producto)
    return db_producto

def delete_producto(db: Session, producto_id: int):
    db_producto = get_producto(db, producto_id)
    if db_producto:
        db.delete(db_producto)
        db.commit()
        return True
    return False

def update_stock_producto(db: Session, producto_id: int, cantidad: int):
    producto = get_producto(db, producto_id)
    if producto:
        producto.stock += cantidad
        db.commit()
        db.refresh(producto)
    return producto

# Alquiler CRUD
def create_alquiler(db: Session, alquiler: schemas.AlquilerCreate):
    # Verificar si existe un alquiler pendiente para este cliente
    alquiler_existente = db.query(models.Alquiler)\
        .filter(
            models.Alquiler.id_cliente == alquiler.id_cliente,
            models.Alquiler.estado == "pendiente"
        )\
        .first()

    if alquiler_existente:
        # Actualizar el alquiler existente
        alquiler_existente.total += alquiler.total
        
        # Agregar nuevos detalles al alquiler existente
        for detalle in alquiler.detalles:
            nuevo_detalle = models.DetalleAlquiler(
                id_alquiler=alquiler_existente.id,
                id_producto=detalle.id_producto,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
                subtotal=detalle.subtotal
            )
            db.add(nuevo_detalle)
        
        db.commit()
        db.refresh(alquiler_existente)
        return alquiler_existente
    
    # Si no existe un alquiler pendiente, crear uno nuevo
    db_alquiler = models.Alquiler(
        id_cliente=alquiler.id_cliente,
        fecha_inicio=alquiler.fecha_inicio,
        fecha_fin=alquiler.fecha_fin,
        total=alquiler.total,
        estado="pendiente"
    )
    db.add(db_alquiler)
    db.commit()
    db.refresh(db_alquiler)

    # Crear los detalles del alquiler
    for detalle in alquiler.detalles:
        db_detalle = models.DetalleAlquiler(
            id_alquiler=db_alquiler.id,
            id_producto=detalle.id_producto,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario,
            subtotal=detalle.subtotal
        )
        db.add(db_detalle)
    
    db.commit()
    db.refresh(db_alquiler)
    return db_alquiler

def get_alquiler(db: Session, alquiler_id: int):
    return db.query(models.Alquiler).filter(models.Alquiler.id == alquiler_id).first()

def get_alquileres(db: Session, skip: int = 0, limit: int = 100):
    # Obtener alquileres ordenados por cliente y fecha
    return db.query(models.Alquiler)\
        .order_by(models.Alquiler.id_cliente, models.Alquiler.fecha_creacion.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_alquileres_cliente(db: Session, cliente_id: int):
    # Obtener alquileres de un cliente específico ordenados por fecha
    return db.query(models.Alquiler)\
        .filter(models.Alquiler.id_cliente == cliente_id)\
        .order_by(models.Alquiler.fecha_creacion.desc())\
        .all()

def update_estado_alquiler(db: Session, alquiler_id: int, nuevo_estado: str):
    db_alquiler = get_alquiler(db, alquiler_id)
    if db_alquiler:
        db_alquiler.estado = nuevo_estado
        if nuevo_estado == "devuelto":
            db_alquiler.fecha_devolucion = datetime.now()
        db.commit()
        db.refresh(db_alquiler)
    return db_alquiler

def delete_alquiler(db: Session, alquiler_id: int):
    db_alquiler = get_alquiler(db, alquiler_id)
    if db_alquiler:
        # Devolver stock de productos
        for detalle in db_alquiler.detalles:
            update_stock_producto(db, detalle.id_producto, detalle.cantidad)
        db.delete(db_alquiler)
        db.commit()
        return True
    return False

# Venta CRUD
def create_venta(db: Session, venta: schemas.VentaCreate):
    # Verificar si existe una venta pendiente para este cliente
    venta_existente = db.query(models.Venta)\
        .filter(
            models.Venta.id_cliente == venta.id_cliente,
            models.Venta.estado == "pendiente"
        )\
        .first()

    if venta_existente:
        # Actualizar la venta existente
        venta_existente.total += venta.total
        
        # Agregar nuevos detalles a la venta existente
        for detalle in venta.detalles:
            nuevo_detalle = models.DetalleVenta(
                id_venta=venta_existente.id,
                id_producto=detalle.id_producto,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
                subtotal=detalle.subtotal
            )
            db.add(nuevo_detalle)
            # Actualizar stock del producto
            update_stock_producto(db, detalle.id_producto, -detalle.cantidad)
        
        db.commit()
        db.refresh(venta_existente)
        return venta_existente
    
    # Si no existe una venta pendiente, crear una nueva
    db_venta = models.Venta(
        id_cliente=venta.id_cliente,
        fecha_venta=datetime.now(),
        total=venta.total,
        estado="pendiente"
    )
    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)

    # Crear los detalles de la venta
    for detalle in venta.detalles:
        db_detalle = models.DetalleVenta(
            id_venta=db_venta.id,
            id_producto=detalle.id_producto,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario,
            subtotal=detalle.subtotal
        )
        db.add(db_detalle)
        # Actualizar stock del producto
        update_stock_producto(db, detalle.id_producto, -detalle.cantidad)
    
    db.commit()
    db.refresh(db_venta)
    return db_venta

def get_venta(db: Session, venta_id: int):
    return db.query(models.Venta).filter(models.Venta.id == venta_id).first()

def get_ventas(db: Session, skip: int = 0, limit: int = 100):
    # Obtener ventas ordenadas por cliente y fecha
    return db.query(models.Venta)\
        .order_by(models.Venta.id_cliente, models.Venta.fecha_venta.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_ventas_cliente(db: Session, cliente_id: int):
    # Obtener ventas de un cliente específico ordenadas por fecha
    return db.query(models.Venta)\
        .filter(models.Venta.id_cliente == cliente_id)\
        .order_by(models.Venta.fecha_venta.desc())\
        .all()

def update_estado_venta(db: Session, venta_id: int, nuevo_estado: str):
    db_venta = get_venta(db, venta_id)
    if db_venta:
        db_venta.estado = nuevo_estado
        if nuevo_estado == "pagado":
            db_venta.fecha_pago = datetime.now()
        db.commit()
        db.refresh(db_venta)
    return db_venta

def delete_venta(db: Session, venta_id: int):
    db_venta = get_venta(db, venta_id)
    if db_venta:
        # Devolver stock de productos
        for detalle in db_venta.detalles:
            update_stock_producto(db, detalle.id_producto, detalle.cantidad)
        db.delete(db_venta)
        db.commit()
        return True
    return False

# Funciones de utilidad
def check_stock_disponible(db: Session, producto_id: int, cantidad: int):
    producto = get_producto(db, producto_id)
    if not producto:
        return False
    return producto.stock >= cantidad 