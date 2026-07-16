from flask import Flask, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_secreta_cambiar_esto"

ESTILO = """
<style>
body {font-family: Arial; background: #f2f2f2;}
.caja {background: white; padding: 20px; margin: 50px auto; width: 320px; border-radius: 8px; text-align:center;}
input, button {width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px;}
button {background: #007BFF; color: white; border: none; cursor: pointer;}
button:hover {background: #0056b3;}
</style>
"""

USUARIO_ADMIN = "admin"
CLAVE_ADMIN = "1234"

# RUTA DE REGISTRO
@app.route("/", methods=["GET", "POST"])
def registro():
    mensaje = ""
    if request.method == "POST":
        nombre = request.form["nombre"]
        cedula = request.form["cedula"]
        correo = request.form["correo"]
        clave = request.form["clave"] # Nueva

        conn = sqlite3.connect("clinica.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pacientes (nombre, cedula, correo, clave) VALUES (?,?,?)",
                       (nombre, cedula, correo, clave))
        conn.commit()
        conn.close()
        return redirect(url_for("login_paciente")) # Lo manda al login después de registrar

    return ESTILO + """
    <div class="caja">
    <h1>Registro Clínica</h1>
    <form method="post">
    <label>Nombre:</label><input name="nombre" required>
    <label>Cedula:</label><input name="cedula" required>
    <label>Correo:</label><input name="correo" type="email" required>
    <label>Contraseña:</label><input name="clave" type="password" required>
    <button type="submit">Enviar</button>
    </form>
    </div>
    """

# LOGIN FALSO PARA PACIENTES
@app.route("/login", methods=["GET", "POST"])
def login_paciente():
    mensaje = ""
    if request.method == "POST":
        # Aquí no validamos nada, solo mostramos el mensaje
        mensaje = "Sistema en mantenimiento. Intente más tarde."

    return ESTILO + f"""
    <div class="caja">
    <h1>Inicio de Sesión Pacientes</h1>
    <form method="post">
    <label>Cedula:</label><input name="cedula" required>
    <label>Contraseña:</label><input name="clave" type="password" required>
    <button type="submit">Ingresar</button>
    </form>
    <p style="color:red; font-weight:bold;">{mensaje}</p>
    </div>
    """

# LOGIN REAL PARA ADMIN
@app.route("/loginadmin", methods=["GET", "POST"])
def login_admin():
    error = ""
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        if usuario == USUARIO_ADMIN and clave == CLAVE_ADMIN:
            session["logueado"] = True
            return redirect(url_for("admin"))
        else:
            error = "Usuario o clave incorrectos"

    return ESTILO + f"""
    <div class="caja">
    <h1>Login Admin</h1>
    <form method="post">
    <label>Usuario:</label><input name="usuario" required>
    <label>Clave:</label><input name="clave" type="password" required>
    <button type="submit">Entrar</button>
    </form>
    <p style="color:red">{error}</p>
    </div>
    """

@app.route("/logout")
def logout():
    session.pop("logueado", None)
    return redirect(url_for("login_admin"))

@app.route("/admin")
def admin():
    if not session.get("logueado"):
        return redirect(url_for("login_admin"))

    conn = sqlite3.connect("clinica.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes ORDER BY id DESC")
    pacientes = cursor.fetchall()
    conn.close()

    filas = ""
    for p in pacientes:
        filas += f"<tr><td>{p[0]}</td><td>{p[1]}</td><td>{p[2]}</td><td>{p[3]}</td></tr>"

    return ESTILO + f"""
    <h1>Pacientes Registrados</h1>
    <a href='/logout'>Cerrar Sesión</a>
    <table>
    <tr><th>ID</th><th>Nombre</th><th>Cedula</th><th>Correo</th></tr>
    {filas}
    </table>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
