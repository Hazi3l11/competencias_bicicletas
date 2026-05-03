from app.db.database import get_connection

# CREATE
def crear_usuario(nombre, email, password, categoria, rol="usuario"):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO usuarios (nombre, email, password, categoria, rol)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nombre, email, password, categoria, rol))
    conn.commit()

    cursor.close()
    conn.close()


# READ (todos)
def obtener_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios")
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()
    return resultados


# READ (uno)
def obtener_usuario(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()
    return resultado


# UPDATE
def actualizar_usuario(id, nombre, email, password, categoria, rol):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE usuarios
    SET nombre = %s, email = %s, password = %s, categoria = %s, rol = %s
    WHERE id = %s
    """
    cursor.execute(query, (nombre, email, password, categoria, rol, id))
    conn.commit()

    cursor.close()
    conn.close()


# DELETE
def eliminar_usuario(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

def obtener_usuario_por_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()
    return usuario