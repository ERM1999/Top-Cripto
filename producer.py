import time
import json
import requests
from kafka import KafkaProducer


# Inicio del productor de Kafka apuntando al contenedor local de Docker
productor = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    # Convertimos automáticamente los diccionarios de Python a texto JSON codificado en UTF-8
    value_serializer=lambda valor: json.dumps(valor).encode('utf-8')
)

nombre_topico = 'precios-crypto'
url_api = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&ids=bitcoin"

print("[PRODUCTOR] Iniciado. Conectando con la API real de CoinGecko...")

try:
    # Bucle infinito para el streaming continuo de datos
    while True:
        try:
            # Petición HTTP GET a la API pública de CoinGecko
            respuesta = requests.get(url_api)
            
            # Verificamos si la respuesta del servidor es correcta (Código 200 OK)
            if respuesta.status_code == 200:
                datos_api = respuesta.json()[0]
                
                # Extracción directa de las métricas financieras en tiempo real
                precio_real = datos_api["current_price"]
                cambio_porcentaje = datos_api["price_change_percentage_24h"]
                capitalizacion_mercado = datos_api["market_cap"]
                volumen_24h = datos_api["total_volume"]
                
                # Evaluación de la tendencia 
                tendencia = "Alcista" if cambio_porcentaje >= 0 else "Bajista"
                
                # Análisis volatilidad y alertas
                if abs(cambio_porcentaje) > 3:
                    volatilidad = "Alta"
                    mensaje_situacion = f"⚠️ Alerta de mercado: Bitcoin muestra una volatilidad alta con un movimiento del {round(cambio_porcentaje, 2)}% en las últimas 24h."
                elif abs(cambio_porcentaje) > 1:
                    volatilidad = "Media"
                    mensaje_situacion = f"📈 Tendencia {tendencia.lower()} moderada. El precio cotiza en los €{precio_real:,} con actividad estable."
                else:
                    volatilidad = "Baja"
                    mensaje_situacion = "🔄 Mercado en consolidación latente. Bitcoin experimenta fluctuaciones mínimas en las últimas horas."
                
                # Simplificación visual de cifras masiva
                capitalizacion_bonita = f"{round(capitalizacion_mercado / 1_000_000_000_000, 2)}T €" if capitalizacion_mercado >= 1_000_000_000_000 else f"{round(capitalizacion_mercado / 1_000_000_000, 2)}B €"
                volumen_bonito = f"{round(volumen_24h / 1_000_000_000, 2)}B €"
                
                # Construcción del payload estructurado en formato JSON ---
                datos_paquete = {
                    "precio_num": precio_real,
                    "precio": f"€{precio_real:,}",
                    "cambio": f"{'+' if cambio_porcentaje >= 0 else ''}{round(cambio_porcentaje, 2)}%",
                    "tendencia": tendencia,
                    "volatilidad": volatilidad,
                    "mensaje": mensaje_situacion,
                    "capitalizacion": capitalizacion_bonita,
                    "volumen": volumen_bonito
                }
                
                # Publicamos el paquete de datos en el tópico de Kafka
                productor.send(nombre_topico, value=datos_paquete)
                print(f" [API -> KAFKA] Precio: {datos_paquete['precio']} | Cap: {datos_paquete['capitalizacion']} | Vol: {datos_paquete['volumen']}")
                
            else:
                # Captura de errores de control de tráfico como el código 429 (Rate Limit)
                print(f"Error de respuesta de la API: Código {respuesta.status_code}")
                
        except Exception as error:
            # Captura cualquier problema de pérdida de conexión a internet o caída del servidor
            print(f" Error crítico en el bucle de red: {error}")
            
        # Pausa estratégica de 20 segundos para no saturar la API pública y evitar bloqueos de IP
        time.sleep(30)

except KeyboardInterrupt:
    # Captura el cierre controlado mediante consola (Ctrl+C)
    print("\nProductor detenido manualmente por el usuario.")