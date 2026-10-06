import aiosqlite
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                full_name TEXT,
                car_model TEXT,
                car_class TEXT,
                service TEXT,
                estimated_price TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def create_booking(user_id: int, username: str, full_name: str, car_model: str, car_class: str, service: str, estimated_price: str, phone: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO bookings (user_id, username, full_name, car_model, car_class, service, estimated_price, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, username, full_name, car_model, car_class, service, estimated_price, phone))
        await db.commit()
        return cursor.lastrowid
