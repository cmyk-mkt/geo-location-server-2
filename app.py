from flask import Flask, request, jsonify
import os
import geopandas as gpd
from shapely.geometry import Polygon

app = Flask(__name__)

# Pasta para salvar os arquivos CSV
POLYGONS_DIR = 'polygons'
os.makedirs(POLYGONS_DIR, exist_ok=True)

@app.route('/insert-polygon', methods=['POST'])
def insert_polygon():
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

    # Criar um GeoDataFrame
    gdf = gpd.GeoDataFrame({'name': [name], 'color': [color], 'geometry': [polygon]})

    # Caminho do arquivo CSV
    csv_path = os.path.join(POLYGONS_DIR, f'{user_ID}.csv')

    # Verificar se o arquivo já existe
    if os.path.exists(csv_path):
        # Carregar o arquivo existente e adicionar o novo polígono
        existing_gdf = gpd.read_file(csv_path)
        gdf = gpd.GeoDataFrame(existing_gdf.append(gdf, ignore_index=True))
    else:
        # Criar um novo arquivo CSV
        gdf.crs = 'EPSG:4326'  # Definir o sistema de coordenadas

    # Salvar o GeoDataFrame em um arquivo CSV
    gdf.to_file(csv_path, driver='CSV')

    return jsonify({'message': 'Polígono salvo com sucesso!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
