from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20))
    direccion = Column(String(200))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    
    alquileres = relationship("Alquiler", back_populates="cliente")
    ventas = relationship("Venta", back_populates="cliente")

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500))
    precio_venta = Column(Float, nullable=False)
    precio_alquiler = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    talla = Column(String(10), nullable=False)
    color = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

class Alquiler(Base):
    __tablename__ = "alquileres"

    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    total = Column(Float, nullable=False)
    estado = Column(String(20), default="pendiente")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    
    cliente = relationship("Cliente", back_populates="alquileres")
    detalles = relationship("DetalleAlquiler", back_populates="alquiler")

class DetalleAlquiler(Base):
    __tablename__ = "detalles_alquiler"

    id = Column(Integer, primary_key=True, index=True)
    id_alquiler = Column(Integer, ForeignKey("alquileres.id"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
   
    alquiler = relationship("Alquiler", back_populates="detalles")
    producto = relationship("Producto")

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    fecha_venta = Column(DateTime, nullable=False, default=datetime.utcnow)
    total = Column(Float, nullable=False)
    estado = Column(String(20), default="pendiente")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    
    cliente = relationship("Cliente", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta")

class DetalleVenta(Base):
    __tablename__ = "detalles_venta"

    id = Column(Integer, primary_key=True, index=True)
    id_venta = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto") 