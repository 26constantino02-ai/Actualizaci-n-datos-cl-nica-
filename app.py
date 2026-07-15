from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('clinica.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS pacientes (id INTEGER PRIMARY KEY, nombre TEXT, cedula TEXT, correo TEXT, fecha TEXT)''')
conn.commit()
conn.close()

ESTILO = '''
<style>
body{font-family:Arial; background:#f0f4f8; margin:0; padding:20px}
.caja{max-width:500px; margin:50px auto; background:white; padding:30px; border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1)}
h1{color:#0d6efd; text-align:center}
input{width:100%; padding:12px; margin:10px 0; border:1px solid #ccc; border-radius:6px; font-size:16px}
button{width:100%; padding:12px; background:#0d6efd; color:white; border:none; border-radius:6px; font-size:16px; cursor:pointer}
button:hover{background:#0b5ed7}
table{width:90%; margin:20px auto; border-collapse:collapse; background:white}
th{background:#0d6efd; color:white; padding:10px}
td{padding:10px; border:1px solid #ddd; text-align:center}
</style>
'''

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        correo = request.form['correo']
        conn = sqlite3.connect('clinica.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pacientes (nombre, cedula, correo, fecha) VALUES (?,?,?, datetime('now'))", (nombre, cedula, correo))
        conn.commit()
        conn.close()
        return ESTILO + "<div class='caja'><h1>✅ Guardado!</h1><p>Datos guardados correctamente</p><a href='/registro'>Registrar otro</a></div>"
    
    return ESTILO + '''
    <div class="caja">
    <h1>Registro Clínica</h1>
    <form method="post">
    <label>Nombre:</label><input name="nombre" required>
    <label>Cedula:</label><input name="cedula" required>
    <label>Correo:</label><input name="correo" type="email" required>
    <button type="submit">Enviar</button>
    </form>
    </div>'''

@app.route('/buscar/<cedula>')
def buscar_paciente(cedula):
    conn = sqlite3.connect('clinica.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes WHERE cedula=?", (cedula,))
    paciente = cursor.fetchone()
    conn.close()
    if paciente:
        return f"Nombre: {paciente[1]}, Cedula: {paciente[2]}, Correo: {paciente[3]}"
    else:
        return "Paciente no encontrado"

@app.route('/admin')
def admin():
    conn = sqlite3.connect('clinica.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes ORDER BY id DESC")
    pacientes = cursor.fetchall()
    conn.close()
    
    filas = ""
    for
