from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import pooling
import os

app = Flask(__name__)

=

dbconfig = {
    "host": os.environ.get("DB_HOST"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_NAME"),
    "port": 3306
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **dbconfig
)

def get_db_connection():
    return connection_pool.get_connection()


@app.route('/')
def registro():
    return render_template('index.html')


@app.route('/registrar', methods=['POST'])
def registrar():
    try:
        nombre = request.form.get('nombre')
        cedula = request.form.get('cedula')
        telefono = request.form.get('telefono')
        tipo_direccion = request.form.get('tipo_direccion')
        numero_direccion = request.form.get('numero_direccion')
        lider = request.form.get('lider')

        # 🔥 Unimos la dirección
        direccion_completa = f"{tipo_direccion} {numero_direccion}"

        db = get_db_connection()
        cursor = db.cursor()

        sql = """
        INSERT INTO rifa 
        (nombre_apellido, telefono, lider, direccion, cedula)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            nombre,
            telefono,
            lider,
            direccion_completa,
            cedula
        ))

        db.commit()

        cursor.close()
        db.close()

        return jsonify({"numero": cursor.lastrowid})

    except Exception as e:
        print("ERROR REGISTRO:", e)
        return jsonify({"mensaje": "Error al registrar"}), 500

@app.route('/consultar/<int:numero>', methods=['GET'])
def consultar(numero):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT nombre_apellido, telefono, lider FROM rifa WHERE id = %s",
            (numero,)
        )

        resultado = cursor.fetchone()

        if resultado:
            return jsonify({
                "nombre": resultado["nombre_apellido"],
                "telefono": resultado["telefono"],
                "lider": resultado["lider"]
            })
        else:
            return jsonify({"nombre": None})

    except Exception as e:
        print("ERROR CONSULTA:", e)
        return jsonify({"nombre": None})
# ======================================

if __name__ == '__main__':
    app.run()


