from fastapi import FastAPI, HTTPException
from app.schemas.usuario import Usuario
from app.models import queries
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "API funcionando"}

# CREATE
@app.post("/usuarios")
def crear(usuario: Usuario):
    queries.crear_usuario(
        usuario.nombre,
        usuario.email,
        usuario.password,
        usuario.categoria
    )
    return {"mensaje": "Usuario creado"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción lo restringes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# READ ALL
@app.get("/usuarios")
def listar():
    return queries.obtener_usuarios()

# READ ONE
@app.get("/usuarios/{id}")
def obtener(id: int):
    usuario = queries.obtener_usuario(id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# UPDATE
@app.put("/usuarios/{id}")
def actualizar(id: int, usuario: Usuario):
    if not queries.obtener_usuario(id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    queries.actualizar_usuario(
        id,
        usuario.nombre,
        usuario.email,
        usuario.password,
        usuario.categoria
    )
    return {"mensaje": "Usuario actualizado"}

# DELETE
@app.delete("/usuarios/{id}")
def eliminar(id: int):
    if not queries.obtener_usuario(id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    queries.eliminar_usuario(id)
    return {"mensaje": "Usuario eliminado"}