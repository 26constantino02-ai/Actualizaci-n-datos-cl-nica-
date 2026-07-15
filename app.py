from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('clinica.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS pacientes (id INTEGER PRIMARY KEY, nombre TEXT, cedula TEXT, correo TEXT, fecha TEXT)''')
conn.commit()
conn.close()

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
        return "Datos guardados correctamente"
    return render_template_string('''<form method="post">Nombre: <input name="nombre"><br>Cedula: <input name="cedula"><br>Correo: <input name="correo"><br><input type="submit"></form>''')

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
    html = "<h1 style='text-align:center'>Pacientes Registrados</h1><table border='1' style='width:90%; margin:auto; border-collapse:collapse;'>"
    html += "<tr><th>ID</th><th>Nombre</th><th>Cedula</th><th>Correo</th><th>Fecha</th></tr>"
    for p in pacientes:
        html += f"<tr><td>{p[0]}</td><td>{p[1]}</td><td>{p[2]}</td><td>{p[3]}</td><td>{p[4]}</td></tr>"
    html += "</table>"
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
