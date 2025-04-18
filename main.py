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
        async def descargar_con_snaptik(link, tipo):
    snaptik_url = "https://snaptik.app/es2"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    data = {
        "url": link
    }

    try:
        async def descargar_con_snaptik(link, tipo):
    snaptik_url = "https://snaptik.app/es2"
    headers = {
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

                download_links = soup.find_all("a", attrs={"target": "_blank", "rel": "nofollow noopener"})

                if not download_links:
                    print("No se encontraron links.")
                    return None

                if tipo == "sinmarca":
                    return download_links[0]["href"] if len(download_links) > 0 else None
                elif tipo == "normal":
                    return download_links[1]["href"] if len(download_links) > 1 else download_links[0]["href"]
                elif tipo == "audio":
                    for link in download_links:
                        if "mp3" in link["href"]:
                            return link["href"]
                    return None

    except Exception as e:
        print(f"Error en descargar_con_snaptik: {e}")
        return None
