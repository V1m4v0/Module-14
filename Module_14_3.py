from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import os

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.add(button)
kb.add(button2)
kb.add(button3)

kb_inline_buy = InlineKeyboardMarkup(resize_keyboard=True)
inline_button1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
inline_button2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
inline_button3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
inline_button4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb_inline_buy.add(inline_button1, inline_button2, inline_button3, inline_button4)

il_kb = InlineKeyboardMarkup()
il_button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
il_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
il_kb.add(il_button)
il_kb.add(il_button2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет, я бот рассчитывающий калории!', reply_markup=kb)

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=il_kb)

@dp.callback_query_handler(text = ['formulas'])
async def get_formulas(call):
    await call.message.answer(f'Формула для расчета калорий: 10*вес(кг) + 6,25*рост(см) - 5*возраст(г)- 161')
    await call.answer()

@dp.callback_query_handler(text = ['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer ('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = (weight * 10) + (6.25 * growth) - (5 * age) - 161
    await message.answer (f'Ваша норма калорий {calories} ккал в день')
    await state.finish()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = [
        (1, 'Product1', 'описание 1', 100),
        (2, 'Product2', 'описание 2', 200),
        (3, 'Product3', 'описание 3', 300),
        (4, 'Product4', 'описание 4', 400)
    ]
    for product in products:
        number, name, description, price = product
        await message.answer(f'Название: {name} | Описание: {description} | Цена: {price}')
        photo_path = f'picture{number}.jpg'
        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as photo:
                await message.answer_photo(photo=photo)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_inline_buy)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler()
async def all_message(message):
    await message.answer("Для начала работы введите команду /start")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)