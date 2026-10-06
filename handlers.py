from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import CAR_CLASSES, SERVICES, ADMIN_ID, DEV_CHANNEL, DEV_BOT, DEV_CONTACT
import database as db
import keyboards as kb
from states import CalcFlowState

router = Router()

# --- СТАРТ И МЕНЮ ---

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    text = (
        "🏎 <b>APEX DETAIL // Демонстрационный шоурум</b>\n\n"
        "Добро пожаловать в демонстрационную систему автостайлинга и премиального детейлинга!\n\n"
        "Этот бот показывает, как современная автостудия решает 3 ключевые задачи:\n"
        "• ⚡ <b>Экспресс-расчет сметы</b> за 20 секунд прямо в мессенджере\n"
        "• 📸 <b>Презентация работ и портфолио</b> без ухода на внешние сайты\n"
        "• 🎯 <b>Защита от простоя боксов</b> и мгновенный сбор горячих броней\n\n"
        "<i>Нажмите кнопку ниже, чтобы протестировать расчет стоимости:</i>"
    )
    await message.answer(text, reply_markup=kb.main_menu_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "to_main")
async def cb_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Главное меню шоурума:",
        reply_markup=kb.main_menu_keyboard()
    )
    await callback.answer()

# --- КАЛЬКУЛЯТОР СТОИМОСТИ ---

@router.message(F.text == "⚡ Рассчитать стоимость (20 сек)")
@router.callback_query(F.data == "calc_start")
async def start_calculator(event: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    text = (
        "⚡ <b>Шаг 1 из 3: Выберите класс вашего автомобиля</b>\n\n"
        "Стоимость и расход материалов зависят от габаритов и площади кузова:"
    )
    keyboard = kb.car_classes_keyboard()
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        await event.answer()
    else:
        await event.answer(text, reply_markup=keyboard, parse_mode="HTML")

@router.callback_query(F.data.startswith("class:"))
async def choose_car_class(callback: CallbackQuery):
    car_class = callback.data.split(":")[1]
    class_info = CAR_CLASSES.get(car_class, {})
    text = (
        f"Вы выбрали: <b>{class_info.get('title')}</b>\n"
        f"<i>Примеры: {class_info.get('examples')}</i>\n\n"
        f"⚡ <b>Шаг 2 из 3: Выберите вашу модель</b> или введите её вручную:"
    )
    await callback.message.edit_text(
        text,
        reply_markup=kb.quick_models_keyboard(car_class),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("model_manual:"))
async def manual_model_input(callback: CallbackQuery, state: FSMContext):
    car_class = callback.data.split(":")[1]
    await state.set_state(CalcFlowState.waiting_for_custom_model)
    await state.update_data(car_class=car_class)
    await callback.message.answer(
        "✏️ Напишите марку и модель вашего авто (например: <i>Porsche Taycan</i> или <i>Lexus RX 350</i>):",
        reply_markup=kb.cancel_calc_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.message(CalcFlowState.waiting_for_custom_model)
async def process_manual_model(message: Message, state: FSMContext):
    model_name = message.text.strip()
    data = await state.get_data()
    car_class = data.get("car_class", "crossover")
    await state.clear()
    
    text = (
        f"Автомобиль: <b>{model_name}</b>\n\n"
        f"⚡ <b>Шаг 3 из 3: Выберите необходимый комплекс защиты:</b>"
    )
    await message.answer(
        text,
        reply_markup=kb.services_keyboard(car_class, model_name),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("model:"))
async def choose_quick_model(callback: CallbackQuery):
    _, car_class, model_name = callback.data.split(":")
    text = (
        f"Автомобиль: <b>{model_name}</b>\n\n"
        f"⚡ <b>Шаг 3 из 3: Выберите необходимый комплекс защиты:</b>"
    )
    await callback.message.edit_text(
        text,
        reply_markup=kb.services_keyboard(car_class, model_name),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("serv:"))
async def show_estimate(callback: CallbackQuery):
    _, car_class, s_code, model_name = callback.data.split(":")
    serv_info = SERVICES.get(s_code, {})
    class_info = CAR_CLASSES.get(car_class, {})
    mult = class_info.get("mult", 1.0)
    
    price_min = int(round(serv_info["base_min"] * mult / 1000) * 1000)
    price_max = int(round(serv_info["base_max"] * mult / 1000) * 1000)
    
    estimate_text = (
        f"📋 <b>РАСЧЕТ СМЕТЫ ДЕТЕЙЛИНГА</b>\n\n"
        f"🏎 <b>Автомобиль:</b> {model_name} ({class_info.get('title')})\n"
        f"🛡 <b>Услуга:</b> {serv_info.get('title')}\n"
        f"⏱ <b>Срок работы:</b> {serv_info.get('time')}\n\n"
        f"💰 <b>Ориентировочная стоимость:</b>\n"
        f"👉 <b>{price_min:,.0f} – {price_max:,.0f} ₽</b>\n\n".replace(",", " ") +
        f"<b>Что входит в комплекс:</b>\n"
        f"{serv_info.get('desc')}\n\n"
        f"🎁 <b>СПЕЦ-БОНУС ПРИ БРОНИ ЧЕРЕЗ TELEGRAM:</b>\n"
        f"<i>Бесплатная гидрофобная обработка стекол «Антидождь» (экономия 6 000 ₽) при бронировании бокса на этой неделе!</i>"
    )
    await callback.message.edit_text(
        estimate_text,
        reply_markup=kb.estimate_result_keyboard(car_class, s_code, model_name),
        parse_mode="HTML"
    )
    await callback.answer()

# --- БРОНИРОВАНИЕ БОКСА ---

@router.callback_query(F.data.startswith("book_start:"))
async def start_booking(callback: CallbackQuery, state: FSMContext):
    _, car_class, s_code, model_name = callback.data.split(":")
    serv_info = SERVICES.get(s_code, {})
    class_info = CAR_CLASSES.get(car_class, {})
    mult = class_info.get("mult", 1.0)
    price_min = int(round(serv_info["base_min"] * mult / 1000) * 1000)
    price_max = int(round(serv_info["base_max"] * mult / 1000) * 1000)
    price_str = f"{price_min:,.0f} - {price_max:,.0f} ₽".replace(",", " ")

    await state.set_state(CalcFlowState.waiting_for_booking_phone)
    await state.update_data(
        car_model=model_name,
        car_class=class_info.get("title", ""),
        service=serv_info.get("title", ""),
        estimated_price=price_str
    )

    await callback.message.answer(
        f"🎯 <b>Фиксация бронирования и бонуса</b>\n\n"
        f"Авто: <b>{model_name}</b>\n"
        f"Услуга: <b>{serv_info.get('title')}</b>\n"
        f"Бонус: <b>«Антидождь» передней полусферы в подарок</b>\n\n"
        f"📱 Отправьте ваш <b>номер телефона</b> (или контактный @username), чтобы администратор закрепил за вами бокс и дату заезда:",
        reply_markup=kb.cancel_calc_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.message(CalcFlowState.waiting_for_booking_phone)
async def process_booking_contact(message: Message, state: FSMContext):
    phone = message.text.strip()
    data = await state.get_data()
    car_model = data.get("car_model", "Не указано")
    car_class = data.get("car_class", "")
    service = data.get("service", "")
    price = data.get("estimated_price", "")
    user = message.from_user

    booking_id = await db.create_booking(
        user_id=user.id,
        username=user.username or "",
        full_name=user.full_name or "",
        car_model=car_model,
        car_class=car_class,
        service=service,
        estimated_price=price,
        phone=phone
    )
    await state.clear()

    # Сообщение клиенту
    await message.answer(
        f"✅ <b>Заявка #{booking_id} успешно принята!</b>\n\n"
        f"Бонус <i>«Антидождь в подарок»</i> зафиксирован за автомобилем <b>{car_model}</b>.\n"
        f"Администратор свяжется с вами по номеру <code>{phone}</code> в течение 10 минут для согласования удобного дня заезда в бокс.\n\n"
        f"📍 Адрес студии: ул. Премиальная, 12, закрытый охраняемый паркинг.",
        reply_markup=kb.main_menu_keyboard(),
        parse_mode="HTML"
    )

    # Уведомление владельцу / администратору
    if ADMIN_ID and ADMIN_ID != 0:
        admin_alert = (
            f"🚨 <b>НОВАЯ ЗАЯВКА ИЗ TELEGRAM-БОТА!</b>\n\n"
            f"👤 <b>Клиент:</b> {user.full_name} (@{user.username or 'без_юзернейма'})\n"
            f"📱 <b>Телефон:</b> <code>{phone}</code>\n"
            f"🏎 <b>Авто:</b> {car_model} ({car_class})\n"
            f"🛡 <b>Услуга:</b> {service}\n"
            f"💰 <b>Смета:</b> {price}\n"
            f"🎁 <b>Бонус:</b> Антидождь в подарок"
        )
        try:
            await message.bot.send_message(ADMIN_ID, admin_alert, parse_mode="HTML")
        except Exception:
            pass

# --- ПОРТФОЛИО И ДО/ПОСЛЕ ---

@router.message(F.text == "📸 Портфолио: ДО / ПОСЛЕ")
async def show_portfolio_menu(message: Message):
    text = (
        "📸 <b>Галерея выполненных проектов</b>\n\n"
        "Мы работаем с автомобилями премиум и люкс сегмента. Выберите категорию, чтобы оценить качество подворотов, блеск и детализацию:"
    )
    await message.answer(text, reply_markup=kb.portfolio_categories_keyboard(), parse_mode="HTML")

@router.callback_query(F.data.startswith("port_view:") | F.data.startswith("portfolio:"))
async def view_portfolio_item(callback: CallbackQuery):
    cat = callback.data.split(":")[1]
    
    if cat in ["risk_zones", "full_poly"]:
        card = (
            "🛡 <b>Кейс: Li Auto L9 // Полная защита в матовый сатин</b>\n\n"
            "• <b>Задача:</b> Полная защита от гравия на трассе и изменение внешнего вида с глянца на глубокий шелковистый мат.\n"
            "• <b>Материал:</b> Полиуретан Stek DynoMatt 215 мкм с эффектом гидрофоба.\n"
            "• <b>Допы:</b> Полный антихром решетки и молдингов в черный глянец, бронирование лобового стекла плёнкой ClearPlex, тонировка задней полусферы Lumar 5%.\n"
            "• <b>Срок работы:</b> 4 рабочих дня.\n"
            "• <b>Гарантия:</b> 7 лет без пожелтения и пузырей."
        )
    elif cat == "ceramic":
        card = (
            "✨ <b>Кейс: Porsche 911 Carrera 4S // Восстановительный детейлинг</b>\n\n"
            "• <b>Задача:</b> Убрать круговую паутинку от некачественных моек и вернуть заводскую глубину цвета GT Silver.\n"
            "• <b>Выполнено:</b> 2-этапная деликатная полировка пастами Rupes + удаление 95% микроцарапин.\n"
            "• <b>Защита:</b> 2 слоя премиального кварцевого состава Gyeon Q2 Mohs + 1 слой керамического гидрофоба Skin.\n"
            "• <b>Результат:</b> Эффект «мокрого лака», зеркальное отражение и мощнейший сброс грязи и воды на скорости."
        )
    else:
        card = (
            "🧼 <b>Кейс: BMW X5 M (F95) // Детейлинг светлого салона</b>\n\n"
            "• <b>Задача:</b> Удалить глубокий синий налёт от джинсов на белой коже Merino Silverstone и восстановить матовость.\n"
            "• <b>Выполнено:</b> Деликатная очистка пеной без щелочи Leather Ultra Clean, озонирование системы кондиционирования, удаление запахов.\n"
            "• <b>Консервация:</b> Керамическая пропитка кожи защитным кремом от трещин, ультрафиолета и последующего окрашивания джинсами на 12 месяцев."
        )
    
    await callback.message.edit_text(
        card,
        reply_markup=kb.portfolio_categories_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

# --- МАТЕРИАЛЫ И ГАРАНТИЯ ---

@router.message(F.text == "🛡 Материалы и Гарантия")
async def show_warranty(message: Message):
    text = (
        "🛡 <b>Стандарты качества и материалы</b>\n\n"
        "Мы принципиально не работаем с дешевым винилом и китайскими гибридами, которые через год желтеют и отдираются вместе с заводским лаком.\n\n"
        "<b>Наши поставщики:</b>\n"
        "• <b>SunTek / Stek / Llumar</b> — чистый 100% термопластичный полиуретан (TPU) толщиной 200–215 мкм с функцией самозатягивания царапин при нагреве феном или на солнце.\n"
        "• <b>Gyeon / Koch Chemie</b> — топовая автохимия для детейлинга и полировки.\n\n"
        "<b>Официальная гарантия:</b>\n"
        "Каждому клиенту выдаётся электронный гарантийный сертификат на <b>7 лет</b> на отсутствие отслоений, пожелтения и пузырей."
    )
    await message.answer(text, reply_markup=kb.main_menu_keyboard(), parse_mode="HTML")

# --- ЛОКАЦИЯ И БОКСЫ ---

@router.message(F.text == "📍 Локация и Боксы")
async def show_location(message: Message):
    text = (
        "📍 <b>О наших боксах:</b>\n\n"
        "• 4 полностью изолированных бокса с мощной приточно-вытяжной вентиляцией и обеспыливанием воздуха (гарантия отсутствия пылинок под пленкой).\n"
        "• Профессиональное дневное освещение CRI 98+ для контроля полировки кузова без голограмм.\n"
        "• Закрытый охраняемый паркинг с видеонаблюдением 24/7.\n"
        "• Лаунж-зона с кофе, напитками и PlayStation 5.\n\n"
        "<b>График работы:</b> Ежедневно с 09:00 до 21:00 (по предварительной записи)."
    )
    await message.answer(text, reply_markup=kb.main_menu_keyboard(), parse_mode="HTML")

# --- ПИТЧ ДЛЯ РАЗРАБОТЧИКА (B2B ПРОДАЖА) ---

@router.message(F.text == "🛠 Заказать такой бот себе")
async def show_b2b_pitch(message: Message):
    text = (
        "⚡ <b>Владельцам и руководителям детейлинг-студий:</b>\n\n"
        "Чувствуете разницу между этим ботом и перепиской в директе?\n\n"
        "• Клиент не ждёт 2 часа, пока администратор выйдет из бокса\n"
        "• Он получает смету за 20 секунд и сам оставляет номер ради бонуса\n"
        "• Вы получаете горячего лида прямо в свой Telegram\n\n"
        "Этот шоурум разработан инженерной студией <b>PXLBOT Studios</b>.\n\n"
        "<b>Условия внедрения в вашу студию:</b>\n"
        "• Полная адаптация под ваши услуги, модели авто и прайс-лист\n"
        "• Срок запуска: <b>3–5 рабочих дней</b>\n"
        "• Чистый код на Python, изолированный сервер, никакой абонентки конструкторам\n"
        "• <b>Окупается с первой же закрытой машины</b>\n\n"
        "👉 Свяжитесь с нами для аудита вашей студии:"
    )
    await message.answer(text, reply_markup=kb.b2b_pitch_keyboard(), parse_mode="HTML")
