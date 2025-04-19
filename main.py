import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import aiohttp
from bs4 import BeautifulSoup

API_TOKEN = os.getenv("API_TOKEN")  # NO pongas el token directamente aquí

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def get_download_options(link):
    buttons = [
        [InlineKeyboardButton("Descarga Normal", callback_data=f"normal|{link}")],
        [InlineKeyboardButton("Sin Marca de Agua", callback_data=f"sinmarca|{link}")],
        [InlineKeyboardButton("Solo Audio MP3", callback_data=f"audio|{link}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message_handler(lambda message: "tiktok.com" in message.text)
async def handle_tiktok_link(message: types.Message):
    await message.reply("Selecciona el tipo de descarga:", reply_markup=get_download_options(message.text))

@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    opcion, link = callback_query.data.split("|")
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Procesando {opcion}...")

    video_url = await descargar_con_snaptik(link, opcion)

    if video_url:
        await bot.send_message(callback_query.from_user.id, f"Aquí está tu descarga:\n{video_url}")
    else:
        await bot.send_message(callback_query.from_user.id, "No se pudo obtener el video. Intenta más tarde.")

async def descargar_con_snaptik(link, tipo):
    url = "https://snaptik.app/es2"
    headers = {"User-Agent": "Mozilla/5.0"}
    data = {"url": link}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as resp:
                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                links = soup.find_all("a", attrs={"target": "_blank", "rel": "nofollow noopener"})

                if not links:
                    return None

                if tipo == "sinmarca":
                    return links[0]["href"] if len(links) > 0 else None
                elif tipo == "normal":
                    return links[1]["href"] if len(links) > 1 else links[0]["href"]
                elif tipo == "audio":
                    for l in links:
                        if "mp3" in l["href"]:
                            return l["href"]
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
