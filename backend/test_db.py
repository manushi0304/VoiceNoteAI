import asyncpg
import asyncio

async def test():
    conn = await asyncpg.connect(
        "postgresql://voicenote:voicenote@localhost:5433/voicenote_db"
    )
    print("✅ DATABASE CONNECTED SUCCESSFULLY")
    await conn.close()

asyncio.run(test())
