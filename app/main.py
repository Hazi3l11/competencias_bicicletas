from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext

from app.schemas.usuario import Usuario
from app.models import queries

app = FastAPI()

# -----------------------
# CONFIGURACIÓN SEGURIDAD
# -----------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# -----------------------
# CORS
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restringe en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# RUTA BASE
# -----------------------
@app.get("/")
def inicio():
    return {"mensaje": "API funcionando"}

# -----------------------
# REGISTER (CREATE)
# -----------------------
@app.post("/usuarios")
def crear(usuario: Usuario):
    password_hash = hash_password(usuario.password)

    queries.crear_usuario(
        usuario.nombre,
        usuario.email,
        password_hash,
        usuario.categoria,
        usuario.rol  # ya tienes default = usuario
    )

    return {"mensaje": "Usuario creado"}

# -----------------------
# LOGIN
# -----------------------
@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    usuario = queries.obtener_usuario_por_email(email)

    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    if not verify_password(password, usuario["password"]):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    return {
        "mensaje": "Login exitoso",
        "usuario": {
            "id": usuario["id"],
            "nombre": usuario["nombre"],
            "rol": usuario["rol"]
        }
    }

# -----------------------
# READ ALL
# -----------------------
@app.get("/usuarios")
def listar():
    return queries.obtener_usuarios()

# -----------------------
# READ ONE
# -----------------------
@app.get("/usuarios/{id}")
def obtener(id: int):
    usuario = queries.obtener_usuario(id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario

# -----------------------
# UPDATE
# -----------------------
@app.put("/usuarios/{id}")
def actualizar(id: int, usuario: Usuario):
    if not queries.obtener_usuario(id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    password_hash = hash_password(usuario.password)

    queries.actualizar_usuario(
        id,
        usuario.nombre,
        usuario.email,
        password_hash,
        usuario.categoria,
        usuario.rol
    )

    return {"mensaje": "Usuario actualizado"}

# -----------------------
# DELETE
# -----------------------
@app.delete("/usuarios/{id}")
def eliminar(id: int):
    if not queries.obtener_usuario(id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    queries.eliminar_usuario(id)
    return {"mensaje": "Usuario eliminado"}

# -----------------------
# ADMIN (PROTEGIDO BÁSICO)
# -----------------------
@app.get("/admin/usuarios")
def ver_todos(rol: str):
    if rol != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")

    return queries.obtener_usuarios()