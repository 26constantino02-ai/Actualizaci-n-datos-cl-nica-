   from flask import Flask, request, render_template_string
   import sqlite3
   from werkzeug.security import generate_password_hash

   app = Flask(__name__)

   def init_db():
       conn = sqlite3.connect('clinica.db')
       cursor = conn.cursor()
       cursor.execute('''CREATE TABLE IF NOT EXISTS pacientes
                         (id INTEGER PRIMARY KEY, nombre TEXT, cedula TEXT UNIQUE, correo TEXT, contraseña TEXT)''')
       conn.commit()
       conn.close()

   init_db()

   @app.route('/registro', methods=['GET', 'POST'])
   def registro():
       if request.method == 'POST':
           nombre = request.form['nombre']
           cedula = request.form['cedula']
           correo = request.form['correo']
           contraseña = request.form['contraseña']
           
           contraseña_segura = generate_password_hash(contraseña)
           
           conn = sqlite3.connect('clinica.db')
           cursor = conn.cursor()
           cursor.execute("INSERT INTO pacientes (nombre, cedula, correo, contraseña) VALUES (?, ?, ?)",
                          (nombre, cedula, correo, contraseña_segura))
           conn.commit()
           conn.close()
           
           return "<h2 style='text-align:center; color:green;'>Datos actualizados!</h2><p style='text-align:center;'>Gracias. Ya puedes cerrar esta ventana.</p>"
       
       return render_template_string('''
       <!DOCTYPE html>
       <html>
       <head>
           <meta name="viewport" content="width=device-width, initial-scale=1">
           <title>Actualización de Datos - Clínica</title>
           <style>
               body { font-family: Arial; padding: 20px; max-width: 400px; margin: auto; background: #f5f5f5; }
               .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
               input, button { width: 100%; padding: 12px; margin: 8px 0; box-sizing: border-box; border: 1px solid #ddd; border-radius: 5px; }
               button { background: #007bff; color: white; border: none; font-size: 16px; cursor: pointer; }
               button:hover { background: #0056b3; }
               label { font-weight: bold; font-size: 14px; }
               .legal { font-size: 12px; }
           </style>
       </head>
       <body>
           <div class="card">
               <h2 style="text-align:center;">Actualización de Datos</h2>
               <p style="text-align:center; font-size:14px;">Confirma tu información para tu próxima cita</p>
               <form method="POST">
                   <label>Nombre Completo:</label>
                   <input name="nombre" required>
                   
                   <label>Cédula:</label>
                   <input name="cedula" required>
                   
                   <label>Correo:</label>
                   <input name="correo" type="email" required>
                   
                   <label>Contraseña:</label>
                   <input name="contraseña" type="password" required>
                   
                   <label class="legal"><input type="checkbox" required> Autorizo el tratamiento de mis datos según Ley 1581 de 2012</label>
                   
                   <button type="submit">Actualizar Datos</button>
               </form>
           </div>
       </body>
       </html>
       ''')

   @app.route('/buscar/<cedula>')
   def buscar_paciente(cedula):
       conn = sqlite3.connect('clinica.db')
       cursor = conn.cursor()
       cursor.execute("SELECT nombre, cedula, correo FROM pacientes WHERE cedula = ?", (cedula,))
       paciente = cursor.fetchone()
       conn.close()
       return str(paciente) if paciente else "Paciente no encontrado"

   if __name__ == '__main__':
       app.run()
