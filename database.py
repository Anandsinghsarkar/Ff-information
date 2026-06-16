from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

# MongoDB Connection
client = AsyncIOMotorClient(MONGO_URI)

db = client["ffinfo_bot"]

users = db["users"]
payments = db["payments"]
transactions = db["transactions"]
settings = db["settings"]


# ==========================
# USER FUNCTIONS
# ==========================

async def create_user(user_id):
    user = await users.find_one({"user_id": user_id})

    if not user:
        await users.insert_one({
            "user_id": user_id,
            "credits": 0,
            "total_purchase": 0,
            "joined": True
        })


async def get_user(user_id):
    return await users.find_one({"user_id": user_id})


async def get_credit(user_id):
    user = await users.find_one({"user_id": user_id})

    if not user:
        await create_user(user_id)
        return 0

    return user.get("credits", 0)


async def add_credit(user_id, amount):
    await users.update_one(
        {"user_id": user_id},
        {"$inc": {"credits": amount}},
        upsert=True
    )


async def remove_credit(user_id, amount):
    await users.update_one(
        {"user_id": user_id},
        {"$inc": {"credits": -amount}}
    )


# ==========================
# PAYMENT FUNCTIONS
# ==========================

async def create_payment(
    user_id,
    amount,
    credit,
    utr
):
    result = await payments.insert_one({
        "user_id": user_id,
        "amount": amount,
        "credit": credit,
        "utr": utr,
        "status": "pending"
    })

    return str(result.inserted_id)


async def get_payment(payment_id):
    from bson import ObjectId

    return await payments.find_one({
        "_id": ObjectId(payment_id)
    })


async def approve_payment(payment_id):
    from bson import ObjectId

    payment = await payments.find_one({
        "_id": ObjectId(payment_id)
    })

    if not payment:
        return False

    if payment["status"] == "approved":
        return False

    await add_credit(
        payment["user_id"],
        payment["credit"]
    )

    await payments.update_one(
        {"_id": ObjectId(payment_id)},
        {"$set": {"status": "approved"}}
    )

    await transactions.insert_one({
        "user_id": payment["user_id"],
        "credit": payment["credit"],
        "amount": payment["amount"],
        "type": "purchase"
    })

    return True


async def reject_payment(payment_id):
    from bson import ObjectId

    await payments.update_one(
        {"_id": ObjectId(payment_id)},
        {"$set": {"status": "rejected"}}
    )


async def get_pending_payments():
    data = []

    async for x in payments.find({
        "status": "pending"
    }):
        data.append(x)

    return data


# ==========================
# STATS
# ==========================

async def total_users():
    return await users.count_documents({})


async def total_payments():
    return await payments.count_documents({
        "status": "approved"
    })


async def total_credits():
    total = 0

    async for user in users.find():
        total += user.get("credits", 0)

    return total


# ==========================
# BROADCAST USERS
# ==========================

async def get_all_users():
    ids = []

    async for user in users.find():
        ids.append(user["user_id"])

    return ids