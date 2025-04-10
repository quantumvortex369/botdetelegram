import requests
import time
import asyncio
from telegram import Bot

# --- CONFIGURA TUS DATOS ---
TELEGRAM_TOKEN = '7694452764:AAFw5xJu8K3wVZ_Ci-e3Irp4MnPCf6Hqxh0'
CHAT_ID = '7726691700'
PRECIO_OBJETIVO = 80000
INTERVALO_MINUTOS = 1

bot = Bot(token=TELEGRAM_TOKEN)

def obtener_precio_btc():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    respuesta = requests.get(url)
    datos = respuesta.json()
    return datos['bitcoin']['usd']

async def enviar_alerta(precio_actual):
    mensaje = f'🚨 ¡ALERTA! El precio de Bitcoin bajó a ${precio_actual:.2f} USD'
    await bot.send_message(chat_id=CHAT_ID, text=mensaje)

async def iniciar_bot():
    print("✅ Bot de BTC iniciado (modo async)...")
    while True:
        try:
            precio = obtener_precio_btc()
            print(f"[{time.strftime('%H:%M:%S')}] BTC: ${precio:.2f}")
            if precio < PRECIO_OBJETIVO:
                await enviar_alerta(precio)
            await asyncio.sleep(INTERVALO_MINUTOS * 60)
        except Exception as e:
            print("❌ Error:", e)
            await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(iniciar_bot())