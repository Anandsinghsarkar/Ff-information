from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import (
    OWNER_USERNAME,
    PAYMENT_LINK,
    PACKAGES
)


# ==========================
# MAIN MENU
# ==========================

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🎮 FFINFO",
                callback_data="ffinfo"
            ),
            InlineKeyboardButton(
                text="💳 My Credit",
                callback_data="my_credit"
            )
        ],
        [
            InlineKeyboardButton(
                text="🛒 Purchase",
                callback_data="purchase"
            ),
            InlineKeyboardButton(
                text="👑 Owner",
                callback_data="owner"
            )
        ]
    ]
)


# ==========================
# PURCHASE MENU
# ==========================

def purchase_menu():

    keyboard = []

    for price, credit in PACKAGES.items():

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"₹{price} ➜ {credit} Credits",
                    callback_data=f"buy_{price}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="🔙 Back",
                callback_data="back_main"
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


# ==========================
# PAYMENT MENU
# ==========================

def payment_menu(price, credit):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Pay Now",
                    url=PAYMENT_LINK
                )
            ],
            [
                InlineKeyboardButton(
                    text="📥 Submit UTR",
                    callback_data=f"utr_{price}_{credit}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Back",
                    callback_data="purchase"
                )
            ]
        ]
    )


# ==========================
# OWNER BUTTON
# ==========================

owner_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="👑 Contact Owner",
                url=f"https://t.me/{OWNER_USERNAME.replace('@','')}"
            )
        ]
    ]
)


# ==========================
# ADMIN PANEL
# ==========================

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Add Credit",
                callback_data="admin_add_credit"
            ),
            InlineKeyboardButton(
                text="➖ Remove Credit",
                callback_data="admin_remove_credit"
            )
        ],
        [
            InlineKeyboardButton(
                text="💰 Pending Payments",
                callback_data="pending_payments"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Stats",
                callback_data="admin_stats"
            ),
            InlineKeyboardButton(
                text="📢 Broadcast",
                callback_data="broadcast"
            )
        ]
    ]
)


# ==========================
# APPROVE / REJECT
# ==========================

def payment_approval(payment_id):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Approve",
                    callback_data=f"approve_{payment_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Reject",
                    callback_data=f"reject_{payment_id}"
                )
            ]
        ]
    )


# ==========================
# BACK BUTTON
# ==========================

back_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔙 Back",
                callback_data="back_main"
            )
        ]
    ]
)