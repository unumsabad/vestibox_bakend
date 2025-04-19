from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vestibox API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints de Cliente
@app.post("/clientes/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente_by_email(db, email=cliente.email)
    if db_cliente:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return crud.create_cliente(db=db, cliente=cliente)

@app.get("/clientes/", response_model=List[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = crud.get_clientes(db, skip=skip, limit=limit)
    return clientes

@app.get("/clientes/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@app.put("/clientes/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(cliente_id: int, cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = crud.update_cliente(db, cliente_id, cliente)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@app.delete("/clientes/{cliente_id}")
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    success = crud.delete_cliente(db, cliente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": "Cliente eliminado"}

# Endpoints de Producto
@app.post("/productos/", response_model=schemas.Producto)
def create_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.create_producto(db=db, producto=producto)

@app.get("/productos/", response_model=List[schemas.Producto])
def read_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    productos = crud.get_productos(db, skip=skip, limit=limit)
    return productos

@app.get("/productos/{producto_id}", response_model=schemas.Producto)
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.get_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@app.put("/productos/{producto_id}", response_model=schemas.Producto)
def update_producto(producto_id: int, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = crud.update_producto(db, producto_id, producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@app.delete("/productos/{producto_id}")
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    success = crud.delete_producto(db, producto_id)
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado"}

# Endpoints de Alquiler
@app.post("/alquileres/", response_model=schemas.Alquiler)
def create_alquiler(alquiler: schemas.AlquilerCreate, db: Session = Depends(get_db)):
    return crud.create_alquiler(db=db, alquiler=alquiler)

@app.get("/alquileres/", response_model=List[schemas.Alquiler])
def read_alquileres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alquileres = crud.get_alquileres(db, skip=skip, limit=limit)
    return alquileres

@app.get("/alquileres/{alquiler_id}", response_model=schemas.Alquiler)
def read_alquiler(alquiler_id: int, db: Session = Depends(get_db)):
    db_alquiler = crud.get_alquiler(db, alquiler_id=alquiler_id)
    if db_alquiler is None:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")
    return db_alquiler

@app.put("/alquileres/{alquiler_id}/estado")
def update_estado_alquiler(alquiler_id: int, estado: str, db: Session = Depends(get_db)):
    db_alquiler = crud.update_estado_alquiler(db, alquiler_id, estado)
    if db_alquiler is None:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")
    return db_alquiler

@app.delete("/alquileres/{alquiler_id}")
def delete_alquiler(alquiler_id: int, db: Session = Depends(get_db)):
    success = crud.delete_alquiler(db, alquiler_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alquiler no encontrado")
    return {"message": "Alquiler eliminado"}

@app.get("/alquileres/cliente/{cliente_id}", response_model=List[schemas.Alquiler])
def read_alquileres_cliente(cliente_id: int, db: Session = Depends(get_db)):
    alquileres = crud.get_alquileres_cliente(db, cliente_id)
    return alquileres

# Endpoints de Venta
@app.post("/ventas/", response_model=schemas.Venta)
def create_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    return crud.create_venta(db=db, venta=venta)

@app.get("/ventas/", response_model=List[schemas.Venta])
def read_ventas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ventas = crud.get_ventas(db, skip=skip, limit=limit)
    return ventas

@app.get("/ventas/{venta_id}", response_model=schemas.Venta)
def read_venta(venta_id: int, db: Session = Depends(get_db)):
    db_venta = crud.get_venta(db, venta_id=venta_id)
    if db_venta is None:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return db_venta

@app.put("/ventas/{venta_id}/estado")
def update_estado_venta(venta_id: int, estado: str, db: Session = Depends(get_db)):
    db_venta = crud.update_estado_venta(db, venta_id, estado)
    if db_venta is None:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return db_venta

@app.delete("/ventas/{venta_id}")
def delete_venta(venta_id: int, db: Session = Depends(get_db)):
    success = crud.delete_venta(db, venta_id)
    if not success:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return {"message": "Venta eliminada"}

@app.get("/ventas/cliente/{cliente_id}", response_model=List[schemas.Venta])
def read_ventas_cliente(cliente_id: int, db: Session = Depends(get_db)):
    ventas = crud.get_ventas_cliente(db, cliente_id)
    return ventas

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 