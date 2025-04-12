from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from pydantic import validator

# Cliente Schemas
class ClienteBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    activo: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True

# Producto Schemas
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_venta: float
    precio_alquiler: float
    stock: int = 0
    talla: str
    color: str

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True

# DetalleAlquiler Schemas
class DetalleAlquilerBase(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: float
    subtotal: float

class DetalleAlquilerCreate(DetalleAlquilerBase):
    pass

class DetalleAlquiler(DetalleAlquilerBase):
    id: int
    id_alquiler: int

    class Config:
        from_attributes = True

# Alquiler Schemas
class AlquilerBase(BaseModel):
    id_cliente: int
    fecha_inicio: datetime
    fecha_fin: datetime
    total: float

class AlquilerCreate(AlquilerBase):
    detalles: List[DetalleAlquilerCreate]

    @validator('detalles')
    def validar_detalles(cls, v):
        if not v:
            raise ValueError("El alquiler debe tener al menos un producto")
        return v

class Alquiler(AlquilerBase):
    id: int
    estado: str
    fecha_creacion: datetime
    detalles: List[DetalleAlquiler]

    class Config:
        from_attributes = True

# DetalleVenta Schemas
class DetalleVentaBase(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: float
    subtotal: float

class DetalleVentaCreate(DetalleVentaBase):
    pass

class DetalleVenta(DetalleVentaBase):
    id: int
    id_venta: int

    class Config:
        from_attributes = True

# Venta Schemas
class VentaBase(BaseModel):
    id_cliente: int
    total: float

class VentaCreate(VentaBase):
    detalles: List[DetalleVentaCreate]

    @validator('detalles')
    def validar_detalles(cls, v):
        if not v:
            raise ValueError("La venta debe tener al menos un producto")
        return v

class Venta(VentaBase):
    id: int
    fecha_venta: datetime
    estado: str
    fecha_creacion: datetime
    detalles: List[DetalleVenta]

    class Config:
        from_attributes = True 