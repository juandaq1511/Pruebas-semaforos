from flask import Flask, request, jsonify
from flask_cors import CORS  # Para permitir peticiones de otros dominios
import openai
import os

# Carga la API key desde una variable de entorno (mejor seguridad)
OPENAI_API_KEY = os.getenv("ingresa la api acá juanda")

if not OPENAI_API_KEY:
    raise ValueError("Debes definir la variable de entorno OPENAI_API_KEY con tu clave de OpenAI.")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)
CORS(app)  # Permite peticiones desde el frontend

@app.route("/procesar_trafico", methods=["POST"])
def procesar_trafico():
    try:
        data = request.json
        semaforo_1 = data.get("semaforo_1", {})
        semaforo_2 = data.get("semaforo_2", {})

        prompt = f"""
        Eres un experto en optimización de tráfico. Basado en el estado de los siguientes semáforos:
        - Semáforo 1: {semaforo_1}
        - Semáforo 2: {semaforo_2}

        Calcula los tiempos óptimos en segundos para cada semáforo y devuelve la respuesta en formato JSON:
        {{
            "semaforo_1": tiempo_en_segundos,
            "semaforo_2": tiempo_en_segundos
        }}
        """

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en optimización de tráfico."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extraer la respuesta generada por OpenAI
        decision_text = response.choices[0].message.content.strip()

        # Convertir la respuesta en JSON válido
        try:
            decision_json = eval(decision_text)  # ¡PELIGROSO! Mejor usa json.loads si el formato está garantizado.
        except Exception:
            return jsonify({"error": "La IA no devolvió un JSON válido", "respuesta": decision_text}), 500

        return jsonify(decision_json)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Rutas disponibles:", app.url_map)
    app.run(debug=True)













