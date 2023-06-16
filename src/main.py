import datetime
from typing import List

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from sqlalchemy import case

from models.audience import Audience
from src.config import API_TOKEN
from src.database import Session, engine

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

session = Session(bind=engine)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет!\n"
        "Я помогу найти твоего любимого преподавателя!\n"
        "Отправь мне любое сообщение, а я тебе обязательно отвечу."
    )


def create_pagination_keyboard(current_index: int, array_length: int) -> InlineKeyboardMarkup:
    # Создаем кнопки "Назад" и "Вперед"
    previous_button = InlineKeyboardButton("Назад", callback_data="previous")
    next_button = InlineKeyboardButton("Вперед", callback_data="next")

    # Создаем кнопки с номерами страниц
    page_buttons = []
    for i in range(max(current_index - 2, 0), min(current_index + 3, array_length)):
        page_buttons.append(InlineKeyboardButton(str(i + 1), callback_data=f"page_{i}"))

    # Создаем объект клавиатуры и добавляем кнопки
    pagination_keyboard = InlineKeyboardMarkup(row_width=3)
    pagination_keyboard.add(previous_button, *page_buttons, next_button)

    return pagination_keyboard


async def pagination_callback_handler(callback_query: CallbackQuery, text_array: List[str], current_index):
    # Получаем текущий номер страницы из callback_data
    current_page = int(callback_query.data.split("_")[1])
    # Выполняем какие-то операции для получения следующей/предыдущей страницы
    if callback_query.data == "previous":
        new_index = max(current_index - 5, 0)
    elif callback_query.data == "next":
        new_index = min(current_index + 5, len(text_array) - 1)
    else:
        new_index = current_index

    new_text = "\n\n".join(text_array[new_index:new_index + 5])
    new_keyboard = create_pagination_keyboard(new_index, len(text_array))
    # new_keyboard =
    # Обновляем текст в сообщении и клавиатуру
    await bot.edit_message_text(new_text, chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id, reply_markup=new_keyboard)


def calculate_parity_week(j):
    date = datetime.date(
        datetime.datetime.today().year,
        datetime.datetime.today().month,
        datetime.datetime.today().day
    )
    if (date + datetime.timedelta(days=j)).weekday() == 6:
        return "Нечётная"
    if (date + datetime.timedelta(days=j)).isocalendar().week % 2 == 1:
        return "Нечётная"
    return "Чётная"


@dp.message_handler()
async def search_teacher(message: types.Message):
    week_days = ["ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА", "ЧЕТВЕРГ", "ПЯТНИЦА", "СУББОТА", "ВОСКРЕСЕНЬЕ"]
    weekday_dict = {}

    for i in range(-1, 6):
        day = (datetime.datetime.today() + datetime.timedelta(days=i + 1)).isocalendar().week % 2
        weekday = week_days[(datetime.datetime.today() + datetime.timedelta(days=i + 1)).weekday()]
        if day % 2 == 0:
            weekday_dict[weekday] = "чёт"
        else:
            weekday_dict[weekday] = "нечёт"

    ordering = case(
        {weekday_val: index for index, weekday_val in enumerate(list(weekday_dict.keys()))},
        value=Audience.day_of_week
    )

    query = ((Audience.day_of_week == list(weekday_dict)[0]) & (Audience.parity == weekday_dict[list(weekday_dict)[0]]))
    for i in range(1, 7):
        query |= ((Audience.day_of_week == list(weekday_dict)[i]) & (
                    Audience.parity == weekday_dict[list(weekday_dict)[i]]))

    results = session.query(Audience).where(
        Audience.event.like(f"%{message.text}%"),
        query
    ).order_by(
        # Audience.day_of_week.in_()
        ordering
    ).limit(20).all()

    print(len(results))
    if len(results) == 0:
        await message.answer("Либо нет либо хз")
    else:
        out = []
        for result in results:
            print(result.event)
            out.append(f"{message.text} проводит занятие в {result.audience} {result.day_of_week}"
                       f" ({result.parity}) c {result.start_of_class} по {result.end_of_class}")

        print(out)
        #
        # length_out = len(out)
        # if length_out > 5:
        #     previous_button = InlineKeyboardButton("Назад", callback_data="previous")
        #     next_button = InlineKeyboardButton("Вперед", callback_data="next")
        #
        #     pagination_keyboard = InlineKeyboardMarkup(row_width=2)
        #     pagination_keyboard.add(previous_button, next_button)
        #
        # page_buttons = [InlineKeyboardButton(str(i), callback_data=f"page_{i}") for i in range(1, length_out // 5 + 1)]
        #
        #     print(page_buttons, length_out // 5 + 1)
        #
        #     await message.answer("\n\n".join(out[:3]), reply_markup=pagination_keyboard)

        await message.answer("\n\n".join(out))
        # await message.answer("test")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
