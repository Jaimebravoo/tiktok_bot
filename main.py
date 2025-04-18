import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import aiohttp
from bs4 import BeautifulSoup

API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def get_download_options(link):
    buttons = [
        [InlineKeyboardButton("Descarga Normal", callback_data=f"normal|{link}")],
        [InlineKeyboardButton("Sin Marca de Agua", callback_data=f"sinmarca|{link}")],
        [InlineKeyboardButton("Solo Audio MP3", callback_data=f"audio|{link}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message_handler(lambda message: 'tiktok.com' in message.text)
async def handle_tiktok_link(message: types.Message):
    await message.reply("Selecciona el tipo de descarga:", reply_markup=get_download_options(message.text))

@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    opcion, link = callback_query.data.split('|')
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Procesando {opcion}...")

    video_url = await descargar_con_snaptik(link, opcion)

    if video_url:
        await bot.send_message(callback_query.from_user.id, f"Aquí está tu descarga:\n{video_url}")
    else:
        await bot.send_message(callback_query.from_user.id, "No se pudo obtener el video. Intenta más tarde.")

async def descargar_con_snaptik(link, tipo):
    snaptik_url = "https://snaptik.app/abc.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0"
    }

    data = {
        "url": link
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(snaptik_url, headers=headers, data=data) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                results = soup.find_all("a", class_="download-link")

                if tipo == "normal":
                    return results[0]["href"] if len(results) >= 1 else None
                elif tipo == "sinmarca":
                    return results[1]["href"] if len(results) >= 2 else None
                elif tipo == "audio":
                    return results[2]["href"] if len(results) >= 3 else None

    except Exception as e:
        print("Error:", e)
        return None

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
