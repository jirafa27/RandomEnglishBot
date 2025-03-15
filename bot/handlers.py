import os

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

from helpers.chatgpt import AIHelper
from helpers.language_utils import Translator
from helpers.redis_utils import RedisClient
from helpers.voice_utils import transcribe

router = Router()
redis_client = RedisClient()
translator = Translator()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    if redis_client.is_in_active_dialog(message.from_user.id):
        await message.answer(
            "Вы уже общаетесь с собеседником. Наберите /stop, чтобы завершить диалог."
        )
    else:
        await message.answer(
            "Привет! Я бот для анонимного общения на английском."
            "Набери /find, чтобы найти собеседника."
        )


@router.message(Command("find"))
async def cmd_find(message: types.Message):
    """
    Поиск анонимного собеседника.
    Если очередь пуста, отправляем пользователя в очередь.
    Если очередь не пуста, соединяем с кем-то из очереди.
    """
    user_id = message.from_user.id
    if redis_client.is_in_active_dialog(user_id):
        await message.answer(
            "Вы уже общаетесь с собеседником. Наберите /stop, чтобы завершить диалог."
        )
        return

    if not redis_client.is_in_waiting_queue(user_id):
        if redis_client.is_waiting_queue_empty(user_id):
            redis_client.add_to_queue(user_id)
            await message.answer("Ожидание собеседника...")
        else:
            partner_id = redis_client.pop_from_queue()
            print("Hey", user_id, partner_id)
            redis_client.set_dialog(user_id, partner_id)
            await message.answer("Собеседник найден! Можете начать общение.")
            await message.bot.send_message(
                partner_id, "Собеседник найден! Можете начать общение."
            )
    else:
        await message.answer("Ожидание собеседника...")


@router.message(Command("stop"))
async def cmd_stop(message: types.Message):
    """
    Завершение текущего диалога.
    Если пользователь не в диалоге, сообщаем об этом.
    Если в диалоге, обнуляем связь и уведомляем собеседника.
    """
    user_id = message.from_user.id

    if not redis_client.is_in_active_dialog(user_id):
        await message.answer("Вы сейчас не находитесь в диалоге.")
        return

    partner_id = redis_client.remove_dialog(user_id)
    await message.answer(
        "Диалог завершён. Наберите /find, чтобы найти нового собеседника."
    )
    await message.bot.send_message(
        partner_id,
        "Ваш собеседник завершил диалог. Наберите /find, чтобы найти другого.",
    )


@router.message(Command("translate"))
async def cmd_translate(message: types.Message) -> None:
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply(
            "Пожалуйста, укажите текст для перевода после команды.\nПример: /translate Hello, how are you?"
        )
        return
    text = parts[1]
    if translator.is_english_text(text):
        try:
            translated = translator.translate_en_ru(text)
            await message.reply(f"Перевод: {translated}")
        except Exception as e:
            await message.reply(f"Ошибка перевода: {e}")
    elif translator.is_russian_text(text):
        try:
            translated = translator.translate_ru_en(text)
            await message.reply(f"Перевод: {translated}")
        except Exception as e:
            await message.reply(f"Ошибка перевода: {e}")
    else:
        await message.reply(
            "Не удалось определить язык текста. Убедитесь, что текст написан на английском или русском языке."
        )


@router.message()
async def relay_message(message: types.Message):
    """
    Любые сообщения пересылаем собеседнику.
    Если пользователь не в диалоге, игнорируем/сообщаем.
    """
    inline_kb_list = [
        [
            InlineKeyboardButton(
                text="Проверить с помощью ИИ", callback_data=f"check_ai"
            )
        ],
        [
            InlineKeyboardButton(
                text="Отправить собеседнику", callback_data=f"send_to_user"
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
    user_id = message.from_user.id
    if redis_client.is_in_active_dialog(user_id):
        await message.answer(
            "Вы сейчас не находитесь в диалоге. Наберите /find, чтобы найти нового собеседника."
        )
        return
    partner_id = redis_client.get_partner(user_id)
    if message.text:
        if not translator.is_english_text(message.text):
            await message.answer("Пишите, пожалуйста, на английском!")
            return
        await message.answer(
            text=f"Вы отправили: {message.text}", reply_markup=keyboard
        )
        # await message.bot.send_message(partner_id, message.text)
    elif message.photo:
        await message.answer("Тут нельзя отправлять фотографии")
    elif message.sticker:
        await message.bot.send_sticker(partner_id, message.sticker.file_id)
    elif message.voice:
        voice = message.voice
        file_id = voice.file_id
        voices_destination = "../voices"
        os.makedirs(voices_destination, exist_ok=True)
        voice_id = message.voice.file_id
        voice = await message.bot.get_file(file_id)
        local_path = f"{voices_destination}/{voice_id}.ogg"
        await message.bot.download_file(voice.file_path, local_path)
        text_of_voice = transcribe(f"../voices/{voice_id}.ogg")
        if not translator.is_english_text(text_of_voice):
            await message.answer("Голосовые тоже должны быть на английском!")
            return
        await message.bot.send_voice(
            chat_id=partner_id,
            voice=FSInputFile(local_path),
            caption=message.caption or "",
        )
        os.remove(local_path)
    elif message.video:
        await message.answer("Тут нельзя отправлять видео")
    elif message.document:
        await message.answer("Тут нельзя отправлять документы")


@router.callback_query(lambda call: call.data.startswith("send_to_user"))
async def check_ai(call: types.CallbackQuery):
    text_to_send = call.message.text.split(":")[1]
    user_id = call.from_user.id
    partner_id = redis_client.get_partner(user_id)
    await call.bot.send_message(partner_id, text_to_send)
    await call.bot.send_message(user_id, "Сообщение отправлено собеседнику")


@router.callback_query(lambda call: call.data.startswith("check_ai"))
async def check_ai(call: types.CallbackQuery):
    user_text = call.message.text.split(":")[1]
    answer_from_ai = AIHelper().correct_text(user_text)

    inline_kb_list = [
        [
            InlineKeyboardButton(
                text="Отправить версию ИИ", callback_data=f"sendAI_version"
            )
        ],
        [
            InlineKeyboardButton(
                text="Изменить мой текст", switch_inline_query_current_chat=user_text
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
    await call.message.answer(answer_from_ai, reply_markup=keyboard)


@router.callback_query(lambda call: call.data.startswith("sendAI_version"))
async def send_ai_version(call: types.CallbackQuery):
    user_id = call.from_user.id
    partner_id = redis_client.get_partner(user_id)
    text_to_send = call.message.text.split("Исправленный текст: ")[1].split(
        "Пояснения: "
    )[0]
    await call.bot.send_message(partner_id, text_to_send)
    await call.bot.send_message(user_id, "Сообщение отправлено собеседнику")
