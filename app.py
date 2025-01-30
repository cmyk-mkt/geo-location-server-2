from flask import Flask, request, jsonify
import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

app = Flask(__name__)

# Pasta para salvar os arquivos CSV
POLYGONS_DIR = 'polygons'
os.makedirs(POLYGONS_DIR, exist_ok=True)

@app.route('/insert-polygon', methods=['POST'])
def insert_polygon():
    try:
        # Receber os dados do frontend
        data = request.json
        user_ID = data.get('user_ID')
        name = data.get('name')
        coordinates = data.get('coordinates')
        color = data.get('color', 'red')  # Cor padrão: vermelho

        # Verificar se os dados estão completos
        if not user_ID or not name or not coordinates:
            return jsonify({'error': 'Dados incompletos'}), 400

        # Converter as coordenadas para um polígono
        polygon = Polygon([(coord['lng'], coord['lat']) for coord in coordinates])

        # Criar um DataFrame (usando Pandas, pois CSV não armazena geometria corretamente)
        df = pd.DataFrame({'name': [name], 'color': [color], 'geometry': [polygon.wkt]})  # Armazena a geometria como WKT

        # Caminho do arquivo CSV
        csv_path = os.path.join(POLYGONS_DIR, f'{user_ID}.csv')

        # Verificar se o arquivo já existe
        if os.path.exists(csv_path):
            existing_df = pd.read_csv(csv_path)
            df = pd.concat([existing_df, df], ignore_index=True)

        # Salvar no formato CSV
        df.to_csv(csv_path, index=False)

        return jsonify({'message': 'Polígono salvo com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
