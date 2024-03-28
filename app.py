from flask import Flask, request, jsonify
from joblib import load
import pandas as pd
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite el acceso CORS a la API

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://localhost/resultados?trusted_connection=yes'
db = SQLAlchemy(app)

# Definir modelo de datos para la base de datos
class Resultados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prediccion_knn = db.Column(db.Integer)
    prediccion_mlp = db.Column(db.Integer)

@app.route('/guardar_csv', methods=['POST'])
def guardar_csv():
    try:
        # Aquí se obtiene el archivo CSV enviado en la solicitud
        archivo = request.files['archivo']

        # Aquí se guarda el archivo CSV en el sistema de archivos
        archivo.save(archivo.filename)

        # Puedes agregar aquí cualquier procesamiento adicional que necesites hacer con el archivo CSV

        return jsonify({'mensaje': 'Archivo CSV guardado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Cargar modelos
knn_model = load('knn_model.joblib')
mlp_model = load('mlp_model.joblib')

# Ruta de la API para recibir datos y realizar predicciones
@app.route('/predecir', methods=['POST'])
def predecir():
    data = request.json

    # Realizar predicciones con los modelos
    prediccion_knn = knn_model.predict([data['datos']])
    prediccion_mlp = mlp_model.predict([data['datos']])

    # Guardar resultados en la base de datos
    resultado = Resultados(prediccion_knn=prediccion_knn[0], prediccion_mlp=prediccion_mlp[0])
    db.session.add(resultado)
    db.session.commit()

    return jsonify({'prediccion_knn': prediccion_knn[0], 'prediccion_mlp': prediccion_mlp[0]})

# Función para agregar resultados a la base de datos y al archivo CSV original
def agregar_resultados_a_csv():
    try:
        resultados = Resultados.query.all()
        df_resultados = pd.DataFrame([(r.prediccion_knn, r.prediccion_mlp) for r in resultados], columns=['prediccion_knn', 'prediccion_mlp'])

        # Leer el archivo CSV original
        df_original = pd.read_csv('C:/Users/danie/Desktop/ejercicio-3/winequality-red.csv')

        # Agregar columnas con las predicciones al archivo original
        df_original['prediccion_knn'] = df_resultados['prediccion_knn']
        df_original['prediccion_mlp'] = df_resultados['prediccion_mlp']

        # Guardar el archivo CSV actualizado
        df_original.to_csv('C:/Users/danie/Desktop/ejercicio-3/winequality-red.csv', index=False)
    except Exception as e:
        print("Error al agregar resultados al archivo CSV y la base de datos:", str(e))

if __name__ == '__main__':
    app.run(debug=True)
