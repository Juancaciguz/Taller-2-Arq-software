from flask import Flask, jsonify
import random
import socket
import os
import boto3

S3_BUCKET = os.environ.get('S3_BUCKET') 
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1') 

try:
    s3_client = boto3.client(
        's3',
        region_name=AWS_REGION
    )
except Exception:
    s3_client = None

def get_s3_image_url(image_key):
    if s3_client and S3_BUCKET:
        return f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{image_key}"
    else:
        return "https://via.placeholder.com/200?text=S3+NO+CONFIGURADO" 

def get_container_id():
    try:
        container_id = socket.gethostname()
    except Exception:
        container_id = "ID_no_disponible"
    return container_id

POKENEAS = [
    {
        "Id": 1,
        "Nombre": "Paisanito",
        "Altura": "1.70m",
        "Habilidad": "Cultura del café",
        "Imagen_Key": "pokenea_1.png",
        "Frase filosófica": "El que no conoce la bandeja paisa, no conoce la vida."
    },
    {
        "Id": 2,
        "Nombre": "Medellinense",
        "Altura": "1.85m",
        "Habilidad": "Eterna primavera",
        "Imagen_Key": "pokenea_2.png",
        "Frase filosófica": "Es mejor un amigo que un peso en el bolsillo... si el amigo tiene moto."
    },
    {
        "Id": 3,
        "Nombre": "Antioqueño",
        "Altura": "1.65m",
        "Habilidad": "Poder de la montaña",
        "Imagen_Key": "pokenea_3.png",
        "Frase filosófica": "La berraquera no se compra, se trae de la casa."
    },
    {
        "Id": 4,
        "Nombre": "Guayabito",
        "Altura": "0.50m",
        "Habilidad": "Vuelo de lorito",
        "Imagen_Key": "pokenea_4.png",
        "Frase filosófica": "En la vida hay que ser como la arepa: redondo, caliente y en todas las mesas."
    },
    {
        "Id": 5,
        "Nombre": "Envigadeño",
        "Altura": "1.75m",
        "Habilidad": "Ajiaco ancestral",
        "Imagen_Key": "pokenea_5.png",
        "Frase filosófica": "El camino se hace al andar... o con un buen colectivo."
    },
    {
        "Id": 6,
        "Nombre": "Sabaneta",
        "Altura": "1.60m",
        "Habilidad": "Aroma a natilla",
        "Imagen_Key": "pokenea_6.png",
        "Frase filosófica": "La vida es más dulce con buñuelo y villancico."
    },
    {
        "Id": 7,
        "Nombre": "Orienteño",
        "Altura": "1.90m",
        "Habilidad": "Clima frío",
        "Imagen_Key": "pokenea_7.png",
        "Frase filosófica": "Con un buen aguardiente y ruana, no hay invierno que aguante."
    },
    {
        "Id": 8,
        "Nombre": "Parcechu",
        "Altura": "1.55m",
        "Habilidad": "Habla rápida",
        "Imagen_Key": "pokenea_8.png",
        "Frase filosófica": "Qué chimba el mañana, pero más chimba el sancocho de hoy."
    },
    {
        "Id": 9,
        "Nombre": "Guaro",
        "Altura": "1.80m",
        "Habilidad": "Fiesta perpetua",
        "Imagen_Key": "pokenea_9.png",
        "Frase filosófica": "El trago no te olvida, tú olvidas el trago."
    },
    {
        "Id": 10,
        "Nombre": "Arriero",
        "Altura": "2.00m",
        "Habilidad": "Muleteo poderoso",
        "Imagen_Key": "pokenea_10.png",
        "Frase filosófica": "Las cargas pesadas se llevan mejor con un tinto y una sonrisa."
    }
]

app = Flask(__name__)

@app.route('/pokenea/data', methods=['GET'])
def pokenea_data():
    pokenea_aleatorio = random.choice(POKENEAS)
    data_json = {
        "id": pokenea_aleatorio["Id"],
        "nombre": pokenea_aleatorio["Nombre"],
        "altura": pokenea_aleatorio["Altura"],
        "habilidad": pokenea_aleatorio["Habilidad"],
        "container_id": get_container_id()
    }
    return jsonify(data_json)

@app.route('/pokenea/web', methods=['GET'])
def pokenea_web():
    pokenea_aleatorio = random.choice(POKENEAS)
    imagen_url = get_s3_image_url(pokenea_aleatorio["Imagen_Key"])
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pokenea del Día</title>
        <style>
            body {{ 
                font-family: 'Inter', sans-serif; 
                text-align: center; 
                padding: 20px; 
                background-color: #f7f9fc;
                display: flex;
                flex-direction: column;
                align-items: center;
                min-height: 100vh;
            }}
            .card {{ 
                background: white; 
                padding: 30px; 
                border-radius: 12px; 
                box-shadow: 0 8px 16px rgba(0,0,0,0.1); 
                display: inline-block; 
                max-width: 400px;
                width: 90%;
            }}
            img {{ 
                width: 200px; 
                height: 200px; 
                border: 6px solid #1a73e8; 
                border-radius: 50%; 
                object-fit: cover;
                margin-bottom: 20px;
            }}
            h1 {{ 
                color: #2c3e50; 
                font-size: 1.5em;
                margin-bottom: 10px;
            }}
            p {{ 
                font-style: italic; 
                color: #e74c3c; 
                font-size: 1.1em;
                border-top: 1px solid #eee;
                padding-top: 15px;
            }}
            .container-info {{ 
                margin-top: 30px; 
                font-size: 0.9em; 
                color: #555; 
                background: #e8f0fe;
                padding: 10px 20px;
                border-radius: 8px;
            }}
            strong {{ color: #1a73e8; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>¡Pokenea '{pokenea_aleatorio["Nombre"]}' te habla!</h1>
            <img src="{imagen_url}" alt="Imagen de {pokenea_aleatorio["Nombre"]}" onerror="this.onerror=null; this.src='https://via.placeholder.com/200?text=S3+Error'">
            <p>"{pokenea_aleatorio["Frase filosófica"]}"</p>
        </div>
        <div class="container-info">
            Aplicación corriendo desde el Contenedor ID: <strong>{get_container_id()}</strong>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)


"""
Pegar en la terminal para ejecutar la aplicación:
 1. En caso de que la terminal sea powershell: $env:S3_BUCKET="s3-bucket-378388076569"
 2. En caso de que la terminal sea powershell: $env:AWS_REGION="us-east-2"
 3. Ejecutar: python app.py
 links:
 - http://localhost:5000/pokenea/data
 - http://localhost:5000/pokenea/web
"""