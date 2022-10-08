# -*- coding: utf-8 -*-
from aiogram.types import ContentType, ChatType
from aiogram import Bot, Dispatcher, executor, types

from youbike import *

bot_token = ''
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(
    commands=['start', 'help'],
    chat_type=[ChatType.PRIVATE])
async def welcome(message: types.Message):
    msg = '*用途*：查詢 YouBike 場站狀態\n\n'
    msg += '*使用方法一*：輸入一個或多個關鍵字查詢，關鍵字間用空白分隔\n'
    msg += '例如：`清華大學`、`交通大學 大學路`\n'
    msg += '查詢的欄位有：\n- 場站名稱\n- 場站地址\n\n'
    msg += f'*使用方法二*：使用 Telegram 傳送 GPS 座標，將回傳方圓 {get_radius(None)} 公尺內最近的五個場站的狀態\n\n'
    msg += '*其他*\n'
    msg += '可以利用 `/radius <距離>` 修改 GPS 搜尋半徑，預設為 600 公尺\n'
    msg += '例如：`/radius 500`（單位為公尺）'
    await message.answer(msg, parse_mode='markdown')


@dp.message_handler(
    commands=['radius'],
    chat_type=[ChatType.PRIVATE])
async def radius(message: types.Message):
    args = message.get_args()
    if len(args) == 0:
        msg = f'目前搜尋半徑：{get_radius(message.from_user.id)} 公尺\n\n'
        msg += '利用 `/radius <距離>` 修改搜尋半徑\n'
        msg += '例如：`/radius 500` （單位為公尺）'
        await message.answer(msg)
    elif not args.isdigit():
        await message.answer('距離只能是大於等於零的整數')
    else:
        r = int(args)
        if r > 20000000:
            await message.answer(f'地球周長也就 40000 公里左右，你設那麼大幹嘛')
        r = min(r, 20000000)
        save_radius(message.from_user.id, r)
        await message.answer(f'搜尋半徑已更新為 {r} 公尺')


@dp.message_handler(
    content_types=[
        ContentType.ANIMATION, ContentType.DICE,
        ContentType.LOCATION, ContentType.PHOTO,
        ContentType.STICKER, ContentType.TEXT
    ],
    chat_type=[ChatType.PRIVATE])
async def search(message: types.Message):
    if message.content_type == ContentType.ANIMATION:
        await message.answer('看不懂 GIF')

    elif message.content_type == ContentType.DICE:
        await message.answer_dice(message.dice.emoji)

    elif message.content_type == ContentType.LOCATION:
        status = await message.answer(f'正在取得方圓 {get_radius(message.from_user.id)} 公尺內最近的五個 YouBike 場站資訊')
        youbike1_stations = get_all_stations(youbike_type=1)
        youbike2_stations = get_all_stations(youbike_type=2)
        coor = {
            'latitude': message.location.latitude,
            'longitude': message.location.longitude
        }
        result1 = get_status_by_coor(youbike1_stations, message.from_user.id, coor)
        result2 = get_status_by_coor(youbike2_stations, message.from_user.id, coor)
        await message.answer(
            f'YouBike 1.0\n-----------------------------\n{result1}',
            disable_web_page_preview=True, parse_mode='markdown')
        await message.answer(
            f'YouBike 2.0\n-----------------------------\n{result2}',
            disable_web_page_preview=True, parse_mode='markdown')
        await status.delete()

    elif message.content_type == ContentType.PHOTO:
        await message.answer('看不懂圖片')

    elif message.content_type == ContentType.STICKER:
        await message.answer_sticker(message.sticker.file_id)

    elif message.content_type == ContentType.TEXT:
        status = await message.answer('正在取得 YouBike 場站資訊')
        youbike1_stations = get_all_stations(youbike_type=1)
        youbike2_stations = get_all_stations(youbike_type=2)
        kw_list = [t.strip() for t in message.text.strip().split(' ')]
        result1 = get_status_by_kw(youbike1_stations, kw_list)
        result2 = get_status_by_kw(youbike2_stations, kw_list)
        await message.answer(
            f'YouBike 1.0\n-----------------------------\n{result1}',
            disable_web_page_preview=True, parse_mode='markdown')
        await message.answer(
            f'YouBike 2.0\n-----------------------------\n{result2}',
            disable_web_page_preview=True, parse_mode='markdown')
        await status.delete()


@dp.edited_message_handler()
async def edited(message: types.Message):
    await message.answer('不要偷編輯訊息')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
