from flask import Flask, render_template, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port=3306
    )

@app.route('/')
def registro():
    return render_template('index.html')  # registro


@app.route('/consulta')
def consulta():
    return render_template('nombre.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    try:
        nombre = request.form.get('nombre')
        cedula = request.form.get('cedula')
        telefono = request.form.get('telefono')
        tipo_direccion = request.form.get('tipo_direccion')
        numero_direccion = request.form.get('numero_direccion')
        lider = request.form.get('lider')

        if not nombre or not telefono or not lider:
            return jsonify({"mensaje": "Faltan datos"}), 400

        db = get_db_connection()
        cursor = db.cursor()

        sql = """
        INSERT INTO rifa 
        (nombre_apellido, telefono, lider, tipo_direccion, numero_direccion, cedula)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            nombre,
            telefono,
            lider,
            tipo_direccion,
            numero_direccion,
            cedula
        ))

        db.commit()

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

if __name__ == '__main__':

    app.run()


