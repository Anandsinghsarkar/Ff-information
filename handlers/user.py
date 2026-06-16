from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import requests

from database import (
    create_user,
    get_credit,
    create_payment
)

from keyboards.menu import (
    main_menu,
    purchase_menu,
    payment_menu,
    owner_menu
)

from config import (
    FF_API,
    OWNER_USERNAME,
    ADMIN_IDS
)

from states import (
    FFInfoState,
    UTRState
)

router = Router()

# Store temp package info
user_package = {}


# ==========================
# START
# ==========================

@router.message(CommandStart())
async def start_cmd(
    message: Message
):
    await create_user(
        message.from_user.id
    )

    await message.answer(
        """
🎮 Welcome To FF INFO BOT

Use buttons below.

🎮 FFINFO
💳 My Credit
🛒 Purchase
👑 Owner
        """,
        reply_markup=main_menu
    )


# ==========================
# FFINFO BUTTON
# ==========================

@router.callback_query(
    F.data == "ffinfo"
)
async def ffinfo_btn(
    call: CallbackQuery,
    state: FSMContext
):

    await state.set_state(
        FFInfoState.waiting_uid
    )

    await call.message.answer(
        "📥 Send Free Fire UID"
    )

    await call.answer()


# ==========================
# UID INPUT
# ==========================

@router.message(
    FFInfoState.waiting_uid
)
async def uid_input(
    message: Message,
    state: FSMContext
):

    uid = message.text.strip()

    await message.answer(
        "🔍 Searching..."
    )

    try:

        url = (
            f"{FF_API}"
            f"?uid={uid}"
            f"&region=ind"
        )

        data = requests.get(
            url,
            timeout=20
        ).json()

        result = (
            data.get("result")
            or data
        )

        basic = result.get(
            "basicInfo",
            {}
        )

        name = basic.get(
            "nickname",
            "Unknown"
        )

        level = basic.get(
            "level",
            "N/A"
        )

        likes = basic.get(
            "liked",
            0
        )

        region = basic.get(
            "region",
            "N/A"
        )

        rank = basic.get(
            "rankingPoints",
            0
        )

        text = f"""
🎮 PLAYER INFO

👤 Name: {name}
🆔 UID: {uid}
⭐ Level: {level}
❤️ Likes: {likes}
🌍 Region: {region}
🏆 Rank Points: {rank}
"""

        await message.answer(
            text
        )

    except Exception as e:

        await message.answer(
            f"❌ Error\n{e}"
        )

    await state.clear()


# ==========================
# MY CREDIT
# ==========================

@router.callback_query(
    F.data == "my_credit"
)
async def my_credit(
    call: CallbackQuery
):

    credit = await get_credit(
        call.from_user.id
    )

    await call.message.answer(
        f"""
💳 YOUR CREDIT

Credits: {credit}
"""
    )

    await call.answer()


# ==========================
# PURCHASE
# ==========================

@router.callback_query(
    F.data == "purchase"
)
async def purchase_btn(
    call: CallbackQuery
):

    await call.message.answer(
        """
🛒 Select Package
""",
        reply_markup=purchase_menu()
    )

    await call.answer()


# ==========================
# BUY PACKAGE
# ==========================

@router.callback_query(
    F.data.startswith("buy_")
)
async def buy_package(
    call: CallbackQuery
):

    price = int(
        call.data.split("_")[1]
    )

    credits = int(
        (price / 20) * 7
    )

    user_package[
        call.from_user.id
    ] = {
        "price": price,
        "credit": credits
    }

    await call.message.answer(
        f"""
💳 Package Selected

Amount: ₹{price}
Credits: {credits}

1. Click Pay Now
2. Complete Payment
3. Submit UTR
""",
        reply_markup=payment_menu(
            price,
            credits
        )
    )

    await call.answer()


# ==========================
# SUBMIT UTR
# ==========================

@router.callback_query(
    F.data.startswith("utr_")
)
async def submit_utr(
    call: CallbackQuery,
    state: FSMContext
):

    await state.set_state(
        UTRState.waiting_utr
    )

    await call.message.answer(
        """
📥 Send UTR Number
"""
    )

    await call.answer()


# ==========================
# RECEIVE UTR
# ==========================

@router.message(
    UTRState.waiting_utr
)
async def receive_utr(
    message: Message,
    state: FSMContext
):

    utr = message.text.strip()

    package = user_package.get(
        message.from_user.id
    )

    if not package:

        await message.answer(
            "❌ Package Not Found"
        )

        return

    payment_id = await create_payment(
        message.from_user.id,
        package["price"],
        package["credit"],
        utr
    )

    text = f"""
💰 NEW PAYMENT

User: {message.from_user.id}

Amount: ₹{package['price']}
Credits: {package['credit']}

UTR:
{utr}

Payment ID:
{payment_id}
"""

    for admin in ADMIN_IDS:

        try:
            await message.bot.send_message(
                admin,
                text
            )
        except:
            pass

    await message.answer(
        """
✅ UTR Submitted

Please Wait For Admin Approval.
"""
    )

    await state.clear()


# ==========================
# OWNER
# ==========================

@router.callback_query(
    F.data == "owner"
)
async def owner_btn(
    call: CallbackQuery
):

    await call.message.answer(
        f"""
👑 Owner

{OWNER_USERNAME}
""",
        reply_markup=owner_menu
    )

    await call.answer()


# ==========================
# BACK
# ==========================

@router.callback_query(
    F.data == "back_main"
)
async def back_main(
    call: CallbackQuery
):

    await call.message.answer(
        "🏠 Main Menu",
        reply_markup=main_menu
    )

    await call.answer()