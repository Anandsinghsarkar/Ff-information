from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram.fsm.context import FSMContext

from config import ADMIN_IDS

from database import (
    add_credit,
    remove_credit,
    approve_payment,
    reject_payment,
    total_users,
    total_payments,
    total_credits,
    get_all_users
)

from keyboards.menu import admin_panel

from states import (
    AddCreditState,
    RemoveCreditState,
    BroadcastState
)

router = Router()


# ==========================
# ADMIN CHECK
# ==========================

def is_admin(user_id):
    return user_id in ADMIN_IDS


# ==========================
# ADMIN PANEL
# ==========================

@router.message(F.text == "/admin")
async def admin_cmd(message: Message):

    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "⚙️ ADMIN PANEL",
        reply_markup=admin_panel
    )


# ==========================
# ADD CREDIT
# ==========================

@router.callback_query(
    F.data == "admin_add_credit"
)
async def add_credit_start(
    call: CallbackQuery,
    state: FSMContext
):

    if not is_admin(call.from_user.id):
        return

    await state.set_state(
        AddCreditState.waiting_user_id
    )

    await call.message.answer(
        "📥 Send User ID"
    )


@router.message(
    AddCreditState.waiting_user_id
)
async def add_credit_user(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        user_id=int(message.text)
    )

    await state.set_state(
        AddCreditState.waiting_amount
    )

    await message.answer(
        "💳 Send Credit Amount"
    )


@router.message(
    AddCreditState.waiting_amount
)
async def add_credit_amount(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    user_id = data["user_id"]
    amount = int(message.text)

    await add_credit(
        user_id,
        amount
    )

    try:
        await message.bot.send_message(
            user_id,
            f"🎉 Admin Added {amount} Credits"
        )
    except:
        pass

    await message.answer(
        "✅ Credit Added"
    )

    await state.clear()


# ==========================
# REMOVE CREDIT
# ==========================

@router.callback_query(
    F.data == "admin_remove_credit"
)
async def remove_credit_start(
    call: CallbackQuery,
    state: FSMContext
):

    if not is_admin(call.from_user.id):
        return

    await state.set_state(
        RemoveCreditState.waiting_user_id
    )

    await call.message.answer(
        "📥 Send User ID"
    )


@router.message(
    RemoveCreditState.waiting_user_id
)
async def remove_credit_user(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        user_id=int(message.text)
    )

    await state.set_state(
        RemoveCreditState.waiting_amount
    )

    await message.answer(
        "➖ Send Amount"
    )


@router.message(
    RemoveCreditState.waiting_amount
)
async def remove_credit_amount(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    user_id = data["user_id"]
    amount = int(message.text)

    await remove_credit(
        user_id,
        amount
    )

    try:
        await message.bot.send_message(
            user_id,
            f"⚠️ Admin Removed {amount} Credits"
        )
    except:
        pass

    await message.answer(
        "✅ Credit Removed"
    )

    await state.clear()


# ==========================
# APPROVE PAYMENT
# ==========================

@router.callback_query(
    F.data.startswith("approve_")
)
async def approve_payment_btn(
    call: CallbackQuery
):

    if not is_admin(call.from_user.id):
        return

    payment_id = call.data.replace(
        "approve_",
        ""
    )

    result = await approve_payment(
        payment_id
    )

    if result:

        await call.message.edit_text(
            "✅ Payment Approved"
        )

    else:

        await call.message.edit_text(
            "❌ Already Processed"
        )


# ==========================
# REJECT PAYMENT
# ==========================

@router.callback_query(
    F.data.startswith("reject_")
)
async def reject_payment_btn(
    call: CallbackQuery
):

    if not is_admin(call.from_user.id):
        return

    payment_id = call.data.replace(
        "reject_",
        ""
    )

    await reject_payment(
        payment_id
    )

    await call.message.edit_text(
        "❌ Payment Rejected"
    )


# ==========================
# STATS
# ==========================

@router.callback_query(
    F.data == "admin_stats"
)
async def stats_btn(
    call: CallbackQuery
):

    if not is_admin(call.from_user.id):
        return

    users = await total_users()
    payments = await total_payments()
    credits = await total_credits()

    text = f"""
📊 BOT STATS

👥 Users: {users}

💰 Approved Payments: {payments}

💳 Total Credits:
{credits}
"""

    await call.message.answer(
        text
    )


# ==========================
# BROADCAST
# ==========================

@router.callback_query(
    F.data == "broadcast"
)
async def broadcast_start(
    call: CallbackQuery,
    state: FSMContext
):

    if not is_admin(call.from_user.id):
        return

    await state.set_state(
        BroadcastState.waiting_message
    )

    await call.message.answer(
        "📢 Send Broadcast Message"
    )


@router.message(
    BroadcastState.waiting_message
)
async def broadcast_send(
    message: Message,
    state: FSMContext
):

    users = await get_all_users()

    sent = 0

    for user in users:

        try:

            await message.bot.send_message(
                user,
                message.text
            )

            sent += 1

        except:
            pass

    await message.answer(
        f"✅ Broadcast Sent To {sent} Users"
    )

    await state.clear()