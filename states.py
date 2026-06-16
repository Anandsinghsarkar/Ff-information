from aiogram.fsm.state import State, StatesGroup


# ==========================
# FFINFO STATE
# ==========================

class FFInfoState(StatesGroup):
    waiting_uid = State()


# ==========================
# UTR SUBMIT STATE
# ==========================

class UTRState(StatesGroup):
    waiting_utr = State()


# ==========================
# ADMIN ADD CREDIT
# ==========================

class AddCreditState(StatesGroup):
    waiting_user_id = State()
    waiting_amount = State()


# ==========================
# ADMIN REMOVE CREDIT
# ==========================

class RemoveCreditState(StatesGroup):
    waiting_user_id = State()
    waiting_amount = State()


# ==========================
# BROADCAST
# ==========================

class BroadcastState(StatesGroup):
    waiting_message = State()


# ==========================
# SEARCH USER
# ==========================

class SearchUserState(StatesGroup):
    waiting_user_id = State()


# ==========================
# FORCE JOIN SETTINGS
# ==========================

class ForceJoinState(StatesGroup):
    waiting_channel = State()


# ==========================
# OWNER SETTINGS
# ==========================

class OwnerState(StatesGroup):
    waiting_username = State()


# ==========================
# PAYMENT PACKAGE
# ==========================

class PaymentState(StatesGroup):
    waiting_package = State()
    waiting_utr = State()


# ==========================
# MANUAL CREDIT SYSTEM
# ==========================

class ManualCreditState(StatesGroup):
    waiting_user = State()
    waiting_credit = State()


# ==========================
# ADMIN MESSAGE USER
# ==========================

class MessageUserState(StatesGroup):
    waiting_user = State()
    waiting_message = State()