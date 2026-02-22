from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="bsfju9vs3mdcjjbrcpar-mysql.services.clever-cloud.com",
        user="u1rpyolrzo4bjxzh",
        password="EKibxS6hn5vWJG6051bT",
        database="bsfju9vs3mdcjjbrcpar",
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
        telefono = request.form.get('telefono')
        lider = request.form.get('lider')

        if not nombre or not telefono or not lider:
            return jsonify({"mensaje": "Faltan datos"}), 400

        db = get_db_connection()
        cursor = db.cursor()

        sql = """
        INSERT INTO rifa (nombre_apellido, telefono, lider)
        VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (nombre, telefono, lider))
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