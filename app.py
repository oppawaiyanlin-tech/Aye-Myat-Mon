import os, secrets
from contextlib import asynccontextmanager
from pathlib import Path
from html import escape
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, Update

TOKEN = os.environ['BOT_TOKEN']
ADMIN_ID = int(os.environ['ADMIN_ID'])
PUBLIC_URL = os.environ['PUBLIC_URL'].rstrip('/')
SECRET = os.environ['WEBHOOK_SECRET']
TITLE = os.getenv('PAGE_TITLE', 'ငါ့ကို ချစ်လားဟင်? 🥺')
INTRO = os.getenv('PAGE_MESSAGE', 'အဖြေလေး ပေးပါဦးနော် 💗')

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(Command('start', 'help'))
async def start(message: Message):
    if not message.from_user or message.from_user.id != ADMIN_ID:
        await message.answer('ဒီ Bot ကို Admin သာ အသုံးပြုနိုင်ပါတယ်။')
        return
    await message.answer('💗 Love Proposal Bot\n\n/link — Website Link ရယူရန်\n/help — အကူအညီ\n\nGIF များကို GitHub ရဲ့ static/gifs/ ထဲမှာ ထည့်ပါ။')

@dp.message(Command('link'))
async def link(message: Message):
    if message.from_user and message.from_user.id == ADMIN_ID:
        await message.answer(f'💌 Love Website:\n{PUBLIC_URL}/')

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(f'{PUBLIC_URL}/telegram/webhook', secret_token=SECRET)
    yield
    await bot.session.close()

app = FastAPI(lifespan=lifespan)
app.mount('/static', StaticFiles(directory='static'), name='static')

@app.post('/telegram/webhook')
async def webhook(request: Request):
    if not secrets.compare_digest(request.headers.get('X-Telegram-Bot-Api-Secret-Token', ''), SECRET):
        raise HTTPException(403)
    data = await request.json()
    update = Update.model_validate(data, context={'bot': bot})
    await dp.feed_update(bot, update)
    return {'ok': True}

@app.get('/', response_class=HTMLResponse)
async def index():
    page = Path('templates/index.html').read_text(encoding='utf-8')
    return HTMLResponse(page.replace('__PAGE_TITLE__', escape(TITLE)).replace('__PAGE_MESSAGE__', escape(INTRO)))

@app.get('/health')
async def health():
    return {'ok': True}
